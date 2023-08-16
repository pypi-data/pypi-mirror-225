import json
import logging
import os
import re
import sys
import traceback
from datetime import datetime
from logging.handlers import HTTPHandler
from urllib import parse as urlparse
from urllib.parse import quote_plus
from urllib.request import urlopen

import pystac
import pytz
import requests
import urllib3
from dateutil.parser import parse
from lxml import etree
from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods

# from pypgstac.migrate import Migrate
from pystac.extensions.datacube import (
    DatacubeExtension,
    DimensionType,
    HorizontalSpatialDimension,
    Variable,
)
from shapely import geometry
from tqdm import tqdm

from . import constants, core, utils

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Harvester(object):
    def __init__(
        self,
        main_catalog_url,  # TDS Catalog url to start harvesting (*)
        stac=None,  # Permitting creation of STAC catalogs (True or False) (*)
        stac_dir=None,  # Directory of saving created STAC catalogs (*)
        logger_handler=None,  # Logger handler (*)
        logger_name=None,  # Logger name (*)
        logger_id=None,  # Logger id (*)
        logger_handler_host=None,  # Logger host (*)
        logger_handler_url=None,  # Logger url (*)
        stac_id="tds2stac",  # STAC catalog ID (optional)
        stac_description="None",  # STAC catalog description (optional)
        collection_id_tuples=None,  # STAC collection ID tuples (optional)
        web_service=None,  # TDS XML-based webservives to start crawling('iso','ncml', and 'wms') (optional)
        datetime_filter=None,  # Datetime-based filtering e.g ["2010-02-18T00:00:00.000Z","2040-02-22T00:00:00.000Z"] (optional)
        # catalog_ingestion=None,  # Ingesting static catalog in STAC-API (True or False) (optional),
        # api_posting=None,  # Posting STAC catalog in STAC-API (True) or ingesting directly into pgSTAC (False) (True or False) (optional)
        aggregated_dataset=None,  # An option for harvesting aggregated datasets in TDS (True or False) (optional)
        aggregated_dataset_url=None,  # Aggregating datasets url address in TDS (URL address) (optional)
    ):
        self.scanned = []  # to skip scanned data in main function
        self.scanned_summary = (
            []
        )  # to skip scanned data in 'datasets_summary' function
        self.catalog = dict()  # Main STAC catalog dictionary
        self.datetime_after = (
            None  # A start time object for filtering datasets
        )
        self.datetime_before = (
            None  # An end time object for filtering datasets
        )
        self.data_num_all = (
            0  # A counter of data in the whole catalog url (logging purpose)
        )
        self.branch_num_all = 0  # A counter of datasets in the whole catalog url (logging purpose)
        self.data_num = 0  # A counter of data in a dataset (logging purpose)
        self.branch_num = 0  # A counter of data in a dataset (logging purpose)
        self.web_service = None  # Default web-service type in the begining
        self.auto_lists = []  # Default list of auto-selected lists
        self.collection_id_tuples = collection_id_tuples  # A list of tuples of auto and manual collection id
        self.logger_handler = logger_handler
        self.logger_name = logger_name
        self.logger_id = logger_id
        self.logger_handler_url = logger_handler_url
        self.logger_handler_host = logger_handler_host

        # using 'xml_processing' we get the catalog URL with
        # XML extension and catalog id and XML content of catalog.

        if self.logger_handler is None:
            self.logger = logging.getLogger("stream_handler")
            self.logger.setLevel(level=logging.DEBUG)
            # self.logger.setLevel(level=logging.WARNING)

            logStreamFormatter = logging.Formatter(
                fmt=f"%(levelname)-8s %(asctime)s \t %(filename)s @function %(funcName)s line %(lineno)s - %(message)s",
            )
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(logStreamFormatter)
            streamHandler.setLevel(logging.DEBUG)
            self.logger.addHandler(streamHandler)
        elif self.logger_handler == "HTTPHandler":
            self.logger = logging.getLogger(
                str(self.logger_name) + "_" + str(self.logger_id)
            )
            self.logger.setLevel(level=logging.DEBUG)
            # self.logger.setLevel(level=logging.WARNING)

            logHttpFormatter = logging.Formatter(
                fmt=f"%(levelname)-8s %(asctime)s \t %(filename)s @function %(funcName)s line %(lineno)s - %(message)s",
            )
            httpHandler = logging.handlers.HTTPHandler(
                host=self.logger_handler_host,
                url=self.logger_handler_url,
                method="POST",
            )
            httpHandler.setFormatter(logHttpFormatter)
            httpHandler.setLevel(logging.DEBUG)

            self.logger.addHandler(httpHandler)

        xml_url_catalog, id_catalog, xml = utils.xml_processing(
            main_catalog_url
        )

        self.logger.info("Start Scanning datasets")
        print("Start Scanning datasets of %s" % xml_url_catalog)

        # This function displays a summary of datasets that are going to harvest
        Scanning = list(self.datasets_summary(xml_url_catalog, xml))

        # Writing description in the first step of scanning
        print(str(self.data_num_all), "data are going to be set as items")
        print(
            str(self.branch_num_all),
            "datasets are going to be set as collction",
        )

        if datetime_filter is not None:
            """Skip TDS datasets out of 'datetime_filter' according
            to 'modified' attribute in `date` tag"""

            if datetime_filter[0] is not None:
                try:
                    datetime_after = datetime.strptime(
                        datetime_filter[0], "%Y-%m-%dT%H:%M:%S.%fZ"
                    )

                    if not isinstance(datetime_after, datetime):
                        self.logger.error(
                            "'datetime_after' parameter have to be a datatime object"
                        )

                    else:
                        if datetime_after.tzinfo:
                            datetime_after = datetime_after.astimezone(
                                pytz.utc
                            )
                        else:
                            datetime_after = datetime_after.replace(
                                tzinfo=pytz.utc
                            )
                    self.datetime_after = datetime_after
                except Exception as e:
                    ex_type, ex_value, ex_traceback = sys.exc_info()
                    # print("Exception type : %s " % ex_type.__name__)
                    # print("Exception message : %s" % ex_value)
                    # print(traceback.format_exc())
                    self.logger.error("%s : %s" % (ex_type.__name__, ex_value))

            if datetime_filter[1] is not None:
                try:
                    datetime_before = datetime.strptime(
                        datetime_filter[1], "%Y-%m-%dT%H:%M:%S.%fZ"
                    )

                    if not isinstance(datetime_before, datetime):
                        self.logger.error(
                            "'datetime_before' parameter have to be a datatime object"
                        )
                    else:
                        if datetime_before.tzinfo:
                            datetime_before = datetime_before.astimezone(
                                pytz.utc
                            )
                        else:
                            datetime_before = datetime_before.replace(
                                tzinfo=pytz.utc
                            )
                    self.datetime_before = datetime_before
                except Exception as e:
                    ex_type, ex_value, ex_traceback = sys.exc_info()
                    # print("Exception type : %s " % ex_type.__name__)
                    # print("Exception message : %s" % ex_value)
                    # print(traceback.format_exc())
                    self.logger.error("%s : %s" % (ex_type.__name__, ex_value))
        if stac is not False:
            """In this part STAC catalogs will be created"""
            self.logger.info("Harvesting datasets is started")

            # Main STAC catalog for linking other items and collections
            self.id_catalog = id_catalog
            self.xml_url_catalog = xml_url_catalog
            # Define an empty STAC catalog
            # Here we should extend the functionality of STAC catalog to fix issue #60
            self.catalog[id_catalog] = pystac.Catalog(
                id=stac_id,
                description="["
                + stac_description
                + "]("
                + utils.xml2html(xml_url_catalog)
                + ")",
            )
            # In cases where user has not defined `web_service`
            if web_service is not None:
                self.web_service = web_service
            else:
                self.auto_lists = constants.webservices_list

            self.aggregated_dataset = aggregated_dataset

            if self.aggregated_dataset is not True:
                self.aggregated_dataset = False
                self.aggregated_dataset_url = None
            else:
                self.aggregated_dataset_url = aggregated_dataset_url
            # All collections will be saved in the `urls` list
            urls = list(
                self.datasets_harvester(xml_url_catalog, web_service, xml)
            )
            if len(urls) != 0:
                ###############################################
                # THE FOLLOWING LINE IS ADDED TO FIX ISSUE #75
                ################################################
                collections = list(self.catalog[id_catalog].get_collections())
                for collection in collections:
                    if len(list(collection.get_all_items())) == 0:
                        self.catalog[id_catalog].remove_child(collection.id)

                # Saving STAC catalog in the `stac_dir` directory
                self.catalog[id_catalog].normalize_hrefs(
                    os.path.join(stac_dir, "stac")
                )
                self.catalog[id_catalog].save(
                    catalog_type=pystac.CatalogType.SELF_CONTAINED
                )
                # self.logger.info(
                #     "Job finished successfully! STAC catalog is created"
                # )
                self.logger.info("Harvesting datasets is finished")

            else:
                self.logger.warning(
                    "Activate services in the requested catalog or choose another service"
                )
                # print(
                #     "Warning: Webservices are not activated for this catalog"
                # )

        # if catalog_ingestion is not False:
        #     self.logger.info("Ingesting catalogs is finished")
        #     """With enabling 'catalog_ingestion' STAC catalogs
        #     , collections and items ingest into the 'pgSTAC'"""
        #     ds2stac_ingester.Ingester(stac_dir, api_posting)
        #     self.logger.info("Ingesting catalogs is finished")

    def datasets_harvester(self, url, web_service, xml_content):
        """This is the main function to create the STAC catalog, collections,
        and items and also is for linking them to each other"""

        footprint_temp = None  # Define initial bounding box
        footprint_temp_point = (
            None  # Define initial time-series location point
        )
        collection_interval_time = (
            []
        )  # An array for collecting all items' datetime

        if url in self.scanned:
            self.logger.warning("Already Scanned %s " % url)
            # print("Already Scanned %s " % url)
            return
        self.scanned.append(url)

        url, catalog_colleciton_id, xml = utils.xml_processing(url)

        ###############################################
        # THE FOLLOWING LINE IS ADDED TO FIX ISSUE #75
        ################################################

        catalog_colleciton_id = self.id_catalog

        tree = etree.XML(xml_content)

        try:
            tree = etree.XML(xml_content)
        except BaseException:
            return
        # Finding datasets and consider each of them as a collection
        branches_main = []

        root = etree.parse(urlopen(url)).getroot()
        for child in root:
            if "dataset" in str(child) and self.aggregated_dataset == False:
                catalogRef_list = [
                    str(c) for c in child if "catalogRef" in str(c)
                ]
                dataset_list = [str(c) for c in child if "dataset" in str(c)]
                for c in child:
                    # it considers catalogRef as a collection
                    if "catalogRef" in str(c):
                        branches_main.append(
                            utils.references_urls(
                                url, c.get("{%s}href" % constants.w3)
                            )
                        )

                        # print(branches_main)
                        collection_id = utils.replacement_func(
                            utils.references_urls(
                                url, c.get("{%s}href" % constants.w3)
                            )
                        )
                        if self.collection_id_tuples is not None:
                            for i in self.collection_id_tuples:
                                if (
                                    i[0] == collection_id
                                    and i[1] != ""
                                    and not i[1].isspace()
                                ):
                                    collection_id = i[1]
                                else:
                                    collection_id = collection_id
                        # creation of collection
                        self.catalog[collection_id] = pystac.Collection(
                            id=collection_id,
                            extent=pystac.Extent(spatial=None, temporal=None),
                            description="[Link to TDS]("
                            + utils.xml2html(url)
                            + ")",
                        )
                        self.catalog[catalog_colleciton_id].add_child(
                            self.catalog[collection_id]
                        )
                    # it considers single data that is adjacent to other catalogRefs in main catalog as a single collection
                    elif "dataset" in str(c) and catalogRef_list != []:
                        branches_main.append(
                            url
                            + "?dataset="
                            + c.get("ID").replace("html", "xml")
                        )

                        collection_id = utils.replacement_func(
                            url
                            + "?dataset="
                            + c.get("ID").replace("html", "xml")
                        )
                        if self.collection_id_tuples is not None:
                            for i in self.collection_id_tuples:
                                if (
                                    i[0] == collection_id
                                    and i[1] != ""
                                    and not i[1].isspace()
                                ):
                                    collection_id = i[1]
                                else:
                                    collection_id = collection_id
                        # creation of collection
                        self.catalog[collection_id] = pystac.Collection(
                            id=collection_id,
                            extent=pystac.Extent(spatial=None, temporal=None),
                            description="[Link to TDS]("
                            + url
                            + "?dataset="
                            + c.get("ID").replace("html", "xml")
                            + ")",
                        )
                        self.catalog[catalog_colleciton_id].add_child(
                            self.catalog[collection_id]
                        )
                # when it harvests a dataset without any catalogRef and sub-dataset
                if (
                    dataset_list != []
                    and catalogRef_list == []
                    and url == self.xml_url_catalog
                ):
                    branches_main.append(utils.html2xml(url))
                    collection_id = utils.replacement_func(
                        url + " Collection".replace("html", "xml")
                    )
                    if self.collection_id_tuples is not None:
                        for i in self.collection_id_tuples:
                            if (
                                i[0] == collection_id
                                and i[1] != ""
                                and not i[1].isspace()
                            ):
                                collection_id = i[1]
                            else:
                                collection_id = collection_id
                    # creation of collection
                    self.catalog[collection_id] = pystac.Collection(
                        id=collection_id,
                        extent=pystac.Extent(spatial=None, temporal=None),
                        description="[Link to TDS]("
                        + url.replace("xml", "html")
                        + ")",
                    )
                    self.catalog[catalog_colleciton_id].add_child(
                        self.catalog[collection_id]
                    )
            if "dataset" in str(child) and self.aggregated_dataset == True:
                branches_main.append(utils.html2xml(url))
                collection_id = utils.replacement_func(
                    url + " Aggregated".replace("html", "xml")
                )
                if self.collection_id_tuples is not None:
                    for i in self.collection_id_tuples:
                        if (
                            i[0] == collection_id
                            and i[1] != ""
                            and not i[1].isspace()
                        ):
                            collection_id = i[1]
                        else:
                            collection_id = collection_id
                    # collection_id = next(
                    #     (v[1] for i, v in enumerate(self.collection_id_tuples) if v[0] == collection_id and v[1]!='' and not v[1].isspace()),
                    #     collection_id,
                    # )
                # creation of collection
                self.catalog[collection_id] = pystac.Collection(
                    id=collection_id,
                    extent=pystac.Extent(spatial=None, temporal=None),
                    description="[Link to TDS]("
                    + url.replace("xml", "html")
                    + ")",
                )

                self.catalog[catalog_colleciton_id].add_child(
                    self.catalog[collection_id]
                )

        # Finding all data in datasets to create items
        data_main = []
        for e in branches_main:
            try:
                url_stat = requests.get(e, None, verify=False)
                content = url_stat.text.encode("utf-8")
            except BaseException:
                continue
            data_main.append(content)
        # This condition displays a summary of dataset that is harvesting
        if branches_main == []:
            self.data_num = self.data_num + len(
                tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata)
            )
        else:
            self.branch_num = self.branch_num + len(
                tree.findall(".//{%s}catalogRef" % constants.unidata)
            )
        # A loop through the nested datasets
        for i, d in enumerate(data_main):
            for dataset in self.datasets_harvester(
                branches_main[i], web_service, d
            ):
                yield dataset

        # This displays status of harvesting datasets and data
        print("Start processing: ", url)
        print(
            self.branch_num,
            "/",
            self.branch_num_all,
            "STAC catalogs are created",
        )
        print(
            self.data_num,
            "/",
            self.data_num_all,
            "STAC items are connected to the related catalog",
        )

        # A loop through data in a dataset to create items
        for elem in tqdm(
            tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata),
            colour="red",
        ):
            # Defining variables in TDS catalog and webservices as an empty parameter
            self.services = []
            self.id = None
            self.name = None
            self.catalog_url = None
            self.extracted_date = None
            variables = {}  # variables in a STAC-Item
            dimensions = {}  # dimensions in a STAC-Item

            # Defining variables to call all vars from a dictioanry
            westBoundLongitude = None
            eastBoundLongitude = None
            northBoundLatitude = None
            southBoundLatitude = None
            beginPosition = None
            endPosition = None
            var = []
            dim = []
            keyword = []
            aName = []
            descriptor = []
            dimensionName = []
            harvesting_vars = {
                "long_min": westBoundLongitude,
                "long_max": eastBoundLongitude,
                "lat_min": southBoundLatitude,
                "lat_max": northBoundLatitude,
                "keyword": keyword,
                "var_lists": aName,
                "var_descs": descriptor,
                "var_dims": dimensionName,
                "time_start": beginPosition,
                "time_end": endPosition,
            }

            # Defining variables for the filling out None values
            westBoundLongitude_temp = None
            eastBoundLongitude_temp = None
            northBoundLatitude_temp = None
            southBoundLatitude_temp = None
            beginPosition_temp = None
            endPosition_temp = None
            keyword_temp = []
            aName_temp = []
            descriptor_temp = []
            dimensionName_temp = []
            harvesting_vars_temp = {
                "long_min": westBoundLongitude_temp,
                "long_max": eastBoundLongitude_temp,
                "lat_min": southBoundLatitude_temp,
                "lat_max": northBoundLatitude_temp,
                "keyword": keyword_temp,
                "var_lists": aName_temp,
                "var_descs": descriptor_temp,
                "var_dims": dimensionName_temp,
                "time_start": beginPosition_temp,
                "time_end": endPosition_temp,
            }

            if "?dataset=" in url:
                data_get = requests.get(
                    str(url),
                    None,
                    verify=False,
                )
            else:
                data_get = requests.get(
                    str(url) + "?dataset=" + str(elem.get("ID")),
                    None,
                    verify=False,
                )

            try:
                tree_data = etree.XML(data_get.text.encode("utf-8"))
            except etree.XMLSyntaxError:
                continue
            else:
                try:
                    # It serves as a function to skip data based on datetime
                    extracted_date = elem.find(
                        './/{%s}date[@type="modified"]' % constants.unidata
                    )
                    if extracted_date is not None:
                        try:
                            self.extracted_date = extracted_date.text
                            dt = parse(extracted_date.text)
                            comp_dt = dt.replace(tzinfo=pytz.utc)
                        except ValueError:
                            continue
                        else:
                            dt = dt.replace(tzinfo=pytz.utc)
                            if (
                                self.datetime_after
                                and dt < self.datetime_after
                            ):
                                continue
                            if (
                                self.datetime_before
                                and dt > self.datetime_before
                            ):
                                continue
                    # bleedfixing datatime in STAC-Colleciton and STAC-Items for aggregated datasets. Should be fixed in the future
                    else:
                        comp_dt = parse(
                            datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fz")
                        ).replace(tzinfo=pytz.utc)

                    dataset = tree_data.find("{%s}dataset" % constants.unidata)
                    self.id = dataset.get("ID")
                    self.name = dataset.get("name")
                    metadata = dataset.find("{%s}metadata" % constants.unidata)
                    self.catalog_url = url.split("?")[0]

                    # Services
                    service_tag = dataset.find(
                        "{%s}serviceName" % constants.unidata
                    )
                    if service_tag is None:
                        if metadata is not None:
                            service_tag = metadata.find(
                                "{%s}serviceName" % constants.unidata
                            )

                    if service_tag is None:
                        # Use services found in the file. FMRC aggs do this.
                        services = tree_data.findall(
                            ".//{%s}service[@serviceType='Compound']"
                            % constants.unidata
                        )
                    else:
                        # Use specific named services
                        services = tree_data.findall(
                            ".//{%s}service[@name='%s']"
                            % (constants.unidata, service_tag.text)
                        )

                    for i, service in enumerate(services):
                        # In TDS version 4 and 5 'Compound' is different
                        if (
                            service.get("serviceType") == "Compound"
                            or service.get("serviceType") == "compound"
                        ):
                            for s in service.findall(
                                "{%s}service" % constants.unidata
                            ):
                                service_url = utils.references_urls(
                                    url, s.get("base")
                                ) + dataset.get("urlPath")
                                if s.get("suffix") is not None:
                                    service_url += s.get("suffix")
                                if s.get("name") in ["iso", "ncml", "uddc"]:
                                    service_url += (
                                        "?dataset=%s&&catalog=%s"
                                        % (
                                            self.id,
                                            quote_plus(self.catalog_url),
                                        )
                                    )
                                if s.get("name") in ["wms"]:
                                    service_url += "?service=WMS&version=1.3.0&request=GetCapabilities"
                                # Check whether the service is in the auto_lists or has been selected by the 'web_service' parameter in the Converter Class.
                                if any(
                                    s in service_url for s in self.auto_lists
                                ) or (
                                    self.web_service is not None
                                    and self.web_service in service_url
                                ):
                                    if self.aggregated_dataset == True:
                                        service_url_html = utils.xml2html(url)
                                    else:
                                        service_url_html = (
                                            utils.xml2html(url)
                                            + "?dataset="
                                            + dataset.get("ID")
                                        )
                                    # To prevent 400 HTTP error
                                    try:
                                        root_nested = etree.parse(
                                            urlopen(service_url)
                                        ).getroot()
                                    except Exception:
                                        (
                                            ex_type,
                                            ex_value,
                                            ex_traceback,
                                        ) = sys.exc_info()
                                        # print("Exception type : %s " % ex_type.__name__)
                                        # print("Exception message : %s" % ex_value)
                                        # print(traceback.format_exc())
                                        self.logger.error(
                                            "%s : %s"
                                            % (ex_type.__name__, ex_value)
                                        )
                                        continue

                                    for tags in root_nested.iter():
                                        # In case the user didn't spcify a web_service
                                        if self.auto_lists != []:
                                            try:
                                                core.harvesting_core(
                                                    tags,
                                                    self.auto_lists[0],
                                                    harvesting_vars,
                                                )
                                            except:
                                                self.logger.warning(
                                                    "NcML service is not activated"
                                                )
                                                try:
                                                    core.harvesting_core(
                                                        tags,
                                                        self.auto_lists[1],
                                                        harvesting_vars_temp,
                                                    )
                                                except:
                                                    self.logger.warning(
                                                        "WMS service is not activated"
                                                    )
                                                    try:
                                                        core.harvesting_core(
                                                            tags,
                                                            self.auto_lists[2],
                                                            harvesting_vars,
                                                        )
                                                    except:
                                                        self.logger.warning(
                                                            "ISO service is not activated"
                                                        )
                                                        continue
                                        else:
                                            # In case the user spcified a web_service
                                            core.harvesting_core(
                                                tags,
                                                self.web_service,
                                                harvesting_vars,
                                            )
                                else:
                                    # self.logger.warning("Activate services in the requested catalog")
                                    self.final_msg = "Activate services in the requested catalog"
                                    continue

                            # Alternative option for filling out the None values
                            for s in service.findall(
                                "{%s}service" % constants.unidata
                            ):
                                service_url = utils.references_urls(
                                    url, s.get("base")
                                ) + dataset.get("urlPath")
                                if s.get("suffix") is not None:
                                    service_url += s.get("suffix")
                                if s.get("name") in ["iso", "ncml", "uddc"]:
                                    service_url += (
                                        "?dataset=%s&&catalog=%s"
                                        % (
                                            self.id,
                                            quote_plus(self.catalog_url),
                                        )
                                    )
                                if s.get("name") in ["wms"]:
                                    service_url += "?service=WMS&version=1.3.0&request=GetCapabilities"

                                const = [
                                    (i, harvesting_vars[i])
                                    for i in constants.constant_list
                                ]
                                appen = [
                                    (i, harvesting_vars[i])
                                    for i in constants.append_list
                                ]
                                if None in const:
                                    root_nested = etree.parse(
                                        urlopen(service_url)
                                    ).getroot()
                                    for tags in root_nested.iter():
                                        core.harvesting_core(
                                            tags,
                                            constants.webservices_list.remove(
                                                self.web_service
                                            )[0],
                                            harvesting_vars_temp,
                                        )
                                        for i, j in const:
                                            if (i, None) != (
                                                i,
                                                harvesting_vars_temp[i],
                                            ):
                                                core.harvesting_core(
                                                    tags,
                                                    constants.webservices_list.remove(
                                                        self.web_service
                                                    )[
                                                        1
                                                    ],
                                                    harvesting_vars_temp,
                                                )
                                if [] in appen:
                                    root_nested = etree.parse(
                                        urlopen(service_url)
                                    ).getroot()
                                    for tags in root_nested.iter():
                                        core.harvesting_core(
                                            tags,
                                            constants.webservices_list.remove(
                                                self.web_service
                                            )[0],
                                            harvesting_vars_temp,
                                        )
                                        for i, j in appen:
                                            if (i, []) != (
                                                i,
                                                harvesting_vars_temp[i],
                                            ):
                                                core.harvesting_core(
                                                    tags,
                                                    constants.webservices_list.remove(
                                                        self.web_service
                                                    )[
                                                        1
                                                    ],
                                                    harvesting_vars_temp,
                                                )

                        # It usually happens when we use iso as web_service
                        if harvesting_vars["keyword"] == []:
                            for i in aName:
                                harvesting_vars["keyword"].append(
                                    harvesting_vars["var_dims"]
                                )
                        elif (
                            harvesting_vars["keyword"] != []
                            and self.web_service == "iso"
                        ):
                            temp = []
                            for i in harvesting_vars["var_lists"]:
                                temp.append(harvesting_vars["keyword"])
                            harvesting_vars["keyword"] = temp

                        # Clearing empty values in lists
                        harvesting_vars["var_lists"] = list(
                            filter(None, harvesting_vars["var_lists"])
                        )
                        harvesting_vars["var_descs"] = list(
                            filter(None, harvesting_vars["var_descs"])
                        )
                        harvesting_vars["var_dims"] = list(
                            filter(None, harvesting_vars["var_dims"])
                        )
                        # Due to appending list in a same time to `dimensionName` in WMS harvesting, we need to flatten the lists
                        if self.web_service == "wms" or self.auto_lists != []:
                            harvesting_vars["var_dims"] = list(
                                dict.fromkeys(
                                    [
                                        item
                                        for sublist in harvesting_vars[
                                            "var_dims"
                                        ]
                                        for item in sublist
                                    ]
                                )
                            )
                        harvesting_vars["keyword"] = list(
                            filter(None, harvesting_vars["keyword"])
                        )

                        # print("keyword", harvesting_vars["keyword"])
                        # print("var_lists", harvesting_vars["var_lists"])
                        # print("var_descs", harvesting_vars["var_descs"])
                        # print("var_dims", harvesting_vars["var_dims"])
                        # print("westBoundLongitude", harvesting_vars["lat_min"])
                        # print("eastBoundLongitude", harvesting_vars["lat_max"])
                        # print("southBoundLatitude", harvesting_vars["long_min"])
                        # print("northBoundLatitude", harvesting_vars["long_max"])
                        # print("beginPosition", harvesting_vars["time_start"])
                        # print("endPosition", harvesting_vars["time_end"])

                        # A condition for longitudes more than 180 e.g. 360 degree. Cause STAC doesn't support longs
                        # more than 180
                        if (
                            float(harvesting_vars["long_min"]) > 180
                            or float(harvesting_vars["long_max"]) > 180
                        ):
                            harvesting_vars["long_min"] = str(
                                float(harvesting_vars["long_min"]) - 180
                            )
                            harvesting_vars["long_max"] = str(
                                float(harvesting_vars["long_max"]) - 180
                            )
                        # A criterion for point or bounding box geogrophical coordination in item creation
                        if (
                            harvesting_vars["long_min"]
                            == harvesting_vars["long_max"]
                            or harvesting_vars["lat_max"]
                            == harvesting_vars["lat_min"]
                        ):
                            boundingBox = [
                                harvesting_vars["long_min"],
                                harvesting_vars["lat_max"],
                            ]
                            bbox_x = list(map(float, boundingBox))
                            footprint = geometry.Point(
                                float(harvesting_vars["long_min"]),
                                float(harvesting_vars["lat_max"]),
                            )

                            if footprint_temp_point is None:
                                footprint_temp_point = footprint
                            footprint_temp_point = geometry.shape(
                                footprint
                            ).union(geometry.shape(footprint_temp_point))

                            collection_bbox = list(footprint_temp_point.bounds)

                        else:
                            boundingBox = [
                                harvesting_vars["long_min"],
                                harvesting_vars["lat_min"],
                                harvesting_vars["long_max"],
                                harvesting_vars["lat_max"],
                            ]
                            bbox_x = list(map(float, boundingBox))
                            footprint = geometry.Polygon(
                                [
                                    [bbox_x[0], bbox_x[1]],
                                    [bbox_x[0], bbox_x[3]],
                                    [bbox_x[2], bbox_x[3]],
                                    [bbox_x[2], bbox_x[1]],
                                ]
                            )
                            if footprint_temp is None:
                                footprint_temp = footprint
                            footprint_temp = geometry.shape(footprint).union(
                                geometry.shape(footprint_temp)
                            )
                            collection_bbox = list(footprint_temp.bounds)

                        # Append date of items to an array to create Temporalextend for collections
                        collection_interval_time.append(
                            datetime.strptime(
                                harvesting_vars["time_start"],
                                "%Y-%m-%dT%H:%M:%SZ",
                            ).replace(tzinfo=pytz.utc)
                        )
                        collection_interval_time.append(
                            datetime.strptime(
                                harvesting_vars["time_end"],
                                "%Y-%m-%dT%H:%M:%SZ",
                            ).replace(tzinfo=pytz.utc)
                        )
                        collection_interval_time = sorted(
                            collection_interval_time
                        )
                        collection_interval_final_time = [
                            collection_interval_time[0],
                            collection_interval_time[-1],
                        ]
                        # Item creation
                        item = pystac.Item(
                            id=utils.replacement_func(elem.get("ID")),
                            geometry=geometry.mapping(footprint),
                            bbox=bbox_x,
                            datetime=comp_dt,
                            properties={},
                        )
                        # Add auxiliary information to items
                        item.common_metadata.start_datetime = (
                            datetime.strptime(
                                harvesting_vars["time_start"],
                                "%Y-%m-%dT%H:%M:%SZ",
                            ).replace(tzinfo=pytz.utc)
                        )
                        item.common_metadata.end_datetime = datetime.strptime(
                            harvesting_vars["time_end"], "%Y-%m-%dT%H:%M:%SZ"
                        ).replace(tzinfo=pytz.utc)
                        item.common_metadata.description = (
                            "[Link to the data in TDS]("
                            + service_url_html
                            + ")"
                        )

                        # Adding web services as assets into items
                        for service in services:
                            if (
                                service.get("serviceType") == "Compound"
                                or service.get("serviceType") == "compound"
                            ):
                                for s in service.findall(
                                    "{%s}service" % constants.unidata
                                ):
                                    service_url = utils.references_urls(
                                        url, s.get("base")
                                    ) + dataset.get("urlPath")

                                    if s.get("suffix") is not None:
                                        service_url += s.get("suffix")
                                    if s.get("name") in [
                                        "iso",
                                        "ncml",
                                        "uddc",
                                    ]:
                                        service_url += (
                                            "?dataset=%s&&catalog=%s"
                                            % (
                                                self.id,
                                                quote_plus(self.catalog_url),
                                            )
                                        )
                                    # fix issue #45 related to defect in WMS link
                                    elif s.get("name") in [
                                        "wms",
                                    ]:
                                        service_url += "?service=WMS&version=1.3.0&request=GetCapabilities"
                                    elif (
                                        s.get("name")
                                        in [
                                            "http",
                                        ]
                                        and self.aggregated_dataset is True
                                        and self.aggregated_dataset_url
                                        is not None
                                    ):
                                        service_url = (
                                            self.aggregated_dataset_url
                                        )
                                        media_type_ = pystac.MediaType.HTML
                                    elif (
                                        s.get("name")
                                        in [
                                            "http",
                                        ]
                                        and self.aggregated_dataset is True
                                        and self.aggregated_dataset_url is None
                                    ):
                                        service_url += "?service=WMS&version=1.3.0&request=GetCapabilities"
                                        media_type_ = pystac.MediaType.HTML

                                    if s.get("name") in ["odap"]:
                                        service_url += ".html"
                                    # Determinatio of Media Type
                                    if s.get("name") in [
                                        "iso",
                                        "ncml",
                                        "wms",
                                        "wcs",
                                        "wfs",
                                        "sos",
                                    ]:
                                        media_type_ = pystac.MediaType.XML
                                    elif (
                                        s.get("name") in ["http"]
                                        and self.aggregated_dataset is not True
                                    ):
                                        media_type_ = "application/netcdf"
                                    elif s.get("name") in [
                                        "dap4",
                                        "odap",
                                        "uddc",
                                    ]:
                                        media_type_ = pystac.MediaType.HTML
                                    else:
                                        media_type_ = pystac.MediaType.TEXT

                                    item.add_asset(
                                        key=s.get("name"),
                                        asset=pystac.Asset(
                                            href=service_url,
                                            # title=without_slash,
                                            media_type=media_type_,
                                        ),
                                    )
                        # applying datacube extension to items
                        cube = DatacubeExtension.ext(item, add_if_missing=True)
                        # Creating dimension and varibles to datacube extension
                        # TODO: temporary we add the following line to avoid error in STAC validation but we need to find a better solution
                        # ISSUE #81
                        DatacubeExtension.remove_from(item)
                        for i, v in enumerate(harvesting_vars["var_lists"]):
                            var.append(
                                Variable(
                                    dict(
                                        type="data",
                                        description=harvesting_vars[
                                            "var_descs"
                                        ][i],
                                        dimensions=harvesting_vars["keyword"][
                                            i
                                        ],
                                    )
                                )
                            )

                        for i, v in enumerate(harvesting_vars["var_lists"]):
                            if (
                                harvesting_vars["var_lists"][i]
                                not in harvesting_vars["var_dims"]
                                and harvesting_vars["var_lists"][i]
                                not in harvesting_vars["keyword"]
                            ):
                                variables[v] = var[i]

                        for i, v in enumerate(harvesting_vars["var_dims"]):
                            if (
                                harvesting_vars["var_dims"][i] == "row"
                                or "lon" in harvesting_vars["var_dims"][i]
                            ):
                                extend_ = [
                                    harvesting_vars["long_min"],
                                    harvesting_vars["long_max"],
                                ]
                                type_ = DimensionType.SPATIAL.value
                                description_ = "longitude"
                                axis_ = "x"
                            elif (
                                harvesting_vars["var_dims"][i] == "column"
                                or "lat" in harvesting_vars["var_dims"][i]
                            ):
                                extend_ = [
                                    harvesting_vars["lat_min"],
                                    harvesting_vars["lat_max"],
                                ]
                                type_ = DimensionType.SPATIAL.value
                                description_ = "latitude"
                                axis_ = "y"
                            elif (
                                harvesting_vars["var_dims"][i] == "temporal"
                                or "time" in harvesting_vars["var_dims"][i]
                                or "t" in harvesting_vars["var_dims"][i]
                            ):
                                extend_ = [
                                    harvesting_vars["time_start"],
                                    harvesting_vars["time_end"],
                                ]
                                type_ = DimensionType.TEMPORAL.value
                                description_ = "time"
                                axis_ = "time"
                            else:
                                extend_ = None
                                type_ = DimensionType.SPATIAL.value
                                description_ = harvesting_vars["var_dims"][i]
                                axis_ = harvesting_vars["var_dims"][i]

                            dim.append(
                                HorizontalSpatialDimension(
                                    properties=dict(
                                        axis=axis_,
                                        extent=extend_,
                                        description=description_,
                                        reference_system="epsg:4326",
                                        type=type_,
                                    )
                                )
                            )
                        for i, v in enumerate(harvesting_vars["var_dims"]):
                            dimensions[v] = dim[i]
                        cube.apply(dimensions=dimensions, variables=variables)
                        # Because Collection does not provide point coordination, this condition was applied.
                        if (
                            collection_bbox[0] == collection_bbox[2]
                            or collection_bbox[1] == collection_bbox[3]
                        ):
                            collection_bbox = [
                                collection_bbox[0] - constants.epilon,
                                collection_bbox[1] - constants.epilon,
                                collection_bbox[2] + constants.epilon,
                                collection_bbox[3] + constants.epilon,
                            ]

                        spatial_extent = pystac.SpatialExtent(
                            bboxes=[collection_bbox]
                        )
                        temporal_extent = pystac.TemporalExtent(
                            intervals=[collection_interval_final_time]
                        )
                        # An empty condition for either Temporal or Spatial extent
                        if (
                            collection_bbox is None
                            or collection_interval_final_time is None
                        ):
                            spatial_extent = pystac.SpatialExtent(
                                bboxes=[(0, 0)]
                            )
                            temporal_extent = pystac.TemporalExtent(
                                intervals=[
                                    [datetime.utcnow(), datetime.utcnow()]
                                ]
                            )

                        collection_item_id = utils.replacement_func(url)
                        # the condition below is for the case that we harvest the dataset without sub-datasets
                        if (
                            url == self.xml_url_catalog
                            and self.aggregated_dataset == False
                        ):
                            collection_item_id = (
                                collection_item_id + " Collection"
                            )
                        elif (
                            url == self.xml_url_catalog
                            and self.aggregated_dataset == True
                        ):
                            collection_item_id = (
                                collection_item_id + " Aggregated"
                            )

                        # the condition below is for the case that the collection's id is not the same as the catalog's id
                        # Also it prevents the item to be added to the catalog separately without any connection to the collection
                        if self.collection_id_tuples is not None:
                            for i in self.collection_id_tuples:
                                if (
                                    i[0] == collection_item_id
                                    and i[1] != ""
                                    and not i[1].isspace()
                                ):
                                    collection_item_id = i[1]
                                else:
                                    collection_item_id = collection_item_id
                        if collection_item_id != self.id_catalog:
                            self.catalog[
                                collection_item_id
                            ].extent = pystac.Extent(
                                spatial=spatial_extent,
                                temporal=temporal_extent,
                            )
                            self.catalog[collection_item_id].add_item(item)
                except Exception as e:
                    ex_type, ex_value, ex_traceback = sys.exc_info()
                    # print("Exception type : %s " % ex_type.__name__)
                    # print("Exception message : %s" % ex_value)
                    print(traceback.format_exc())
                    self.logger.critical(
                        "%s : %s" % (ex_type.__name__, ex_value)
                    )

                    continue

            yield str(url) + "?dataset=" + str(elem.get("ID"))
        # When a collection doesn't have Spatial or Temporal extent
        if (
            type(self.catalog[catalog_colleciton_id])
            is pystac.collection.Collection
            and self.catalog[catalog_colleciton_id].extent.spatial is None
        ):
            spatial_extent = pystac.SpatialExtent(bboxes=[[0, 0, 0, 0]])
            temporal_extent = pystac.TemporalExtent(
                intervals=[[datetime.utcnow(), datetime.utcnow()]]
            )
            for elements in list(
                self.catalog[catalog_colleciton_id].get_children()
            ):
                if elements.extent.spatial is not None:
                    self.catalog[
                        catalog_colleciton_id
                    ].extent = elements.extent
                else:
                    self.catalog[catalog_colleciton_id].extent = pystac.Extent(
                        spatial=spatial_extent, temporal=temporal_extent
                    )
            if (
                len(list(self.catalog[catalog_colleciton_id].get_children()))
                == 0
            ):
                self.catalog[catalog_colleciton_id].extent = pystac.Extent(
                    spatial=spatial_extent, temporal=temporal_extent
                )
        if type(self.catalog[catalog_colleciton_id]) is pystac.catalog.Catalog:
            spatial_extent = pystac.SpatialExtent(bboxes=[[0, 0, 0, 0]])
            temporal_extent = pystac.TemporalExtent(
                intervals=[[datetime.utcnow(), datetime.utcnow()]]
            )
            for i in list(self.catalog[catalog_colleciton_id].get_children()):
                if (
                    type(i) is pystac.collection.Collection
                    and i.extent.spatial is None
                ):
                    i.extent = pystac.Extent(
                        spatial=spatial_extent, temporal=temporal_extent
                    )

    def datasets_summary(self, url, xml_content):
        """A function for logging purposes.
        It returns the summary of the datasets in the catalog."""

        if url in self.scanned_summary:
            print("Already Scanned %s " % url)
            return
        self.scanned_summary.append(url)

        url = utils.html2xml(url)

        try:
            tree = etree.XML(xml_content)
        except BaseException:
            return

        branches = []

        for br in tree.findall(".//{%s}catalogRef" % constants.unidata):
            branches.append(
                utils.references_urls(url, br.get("{%s}href" % constants.w3))
            )

        data = []
        for e in branches:
            try:
                url_stat = requests.get(e, None, verify=False)
                content = url_stat.text.encode("utf-8")
            except BaseException:
                print("INFO: Skipping %s (error parsing the XML)" % url)
            data.append(content)

        if branches == []:
            print(
                "|_______",
                url,
                "|  Number of data: ",
                len(
                    tree.findall(
                        ".//{%s}dataset[@urlPath]" % constants.unidata
                    )
                ),
            )
            self.data_num_all = self.data_num_all + len(
                tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata)
            )
        else:
            print(
                "|__",
                url,
                "|  Number of branches: ",
                len(tree.findall(".//{%s}catalogRef" % constants.unidata)),
            )
            self.branch_num_all = self.branch_num_all + len(
                tree.findall(".//{%s}catalogRef" % constants.unidata)
            )

        for i, d in enumerate(data):
            for dataset in self.datasets_summary(branches[i], d):
                yield dataset

        for elem in tree.findall(
            ".//{%s}dataset[@urlPath]" % constants.unidata
        ):
            yield str(url) + "?dataset=" + str(elem.get("ID"))


class Catalog_summary(object):
    """A class for getting the Collection's
    IDs and its Descriptions."""

    def __init__(
        self,
        main_catalog_url,  # TDS Catalog url to start harvesting (*)
        logger_name=None,  # Logger name (*)
        logger_id=None,  # Logger id (*)
        logger_handler_host=None,  # Logger host (*)
        logger_handler_url=None,  # Logger url (*)
        aggregated_dataset=None,  # An option for harvesting aggregated datasets in TDS (True or False) (optional)
    ):
        self.scanned = []  # to skip scanned data in main function
        self.logger_name = logger_name
        self.logger_id = logger_id
        self.logger_handler_url = logger_handler_url
        self.logger_handler_host = logger_handler_host

        # using 'xml_processing' we get the catalog URL with
        # XML extension and catalog id and XML content of catalog.

        self.logger = logging.getLogger(
            str(self.logger_name) + "_" + str(self.logger_id)
        )
        self.logger.setLevel(level=logging.DEBUG)
        # self.logger.setLevel(level=logging.WARNING)

        logHttpFormatter = logging.Formatter(
            fmt=f"%(levelname)-8s %(asctime)s \t %(filename)s @function %(funcName)s line %(lineno)s - %(message)s",
        )
        httpHandler = logging.handlers.HTTPHandler(
            host=self.logger_handler_host,
            url=self.logger_handler_url,
            method="POST",
        )
        httpHandler.setFormatter(logHttpFormatter)
        httpHandler.setLevel(logging.DEBUG)
        self.logger.addHandler(httpHandler)

        xml_url_catalog, id_catalog, xml = utils.xml_processing(
            main_catalog_url
        )

        # self.logger.debug("Getting infos is started")

        # Main STAC catalog for linking other items and collections
        self.id_catalog = id_catalog
        self.xml_url_catalog = xml_url_catalog

        self.aggregated_dataset = aggregated_dataset

        # All collections will be saved in the `urls` list
        urls = list(self.collection_ids(xml_url_catalog, xml))

        # self.logger.debug("Getting infos is finished")

    def collection_ids(self, url, xml_content):
        """This is the main function to get information about collections."""

        if url in self.scanned:
            # self.logger.warning("Already Scanned %s " % url)
            print("Already Scanned %s " % url)
            return
        self.scanned.append(url)

        url, catalog_colleciton_id, xml = utils.xml_processing(url)
        ###############################################
        # THE FOLLOWING LINE IS ADDED TO FIX ISSUE #75
        ################################################

        catalog_colleciton_id = self.id_catalog

        tree = etree.XML(xml_content)

        try:
            tree = etree.XML(xml_content)
        except BaseException:
            return
        # Finding datasets and consider each of them as a collection
        branches_main = []

        root = etree.parse(urlopen(url)).getroot()
        for child in root:
            if "dataset" in str(child) and self.aggregated_dataset == False:
                catalogRef_list = [
                    str(c) for c in child if "catalogRef" in str(c)
                ]
                dataset_list = [str(c) for c in child if "dataset" in str(c)]

                for c in child:
                    # it considers catalogRef as a collection
                    if "catalogRef" in str(c):
                        branches_main.append(
                            utils.references_urls(
                                url, c.get("{%s}href" % constants.w3)
                            )
                        )

                        # print(branches_main)
                        collection_id = utils.replacement_func(
                            utils.references_urls(
                                url, c.get("{%s}href" % constants.w3)
                            )
                        )
                        self.logger.info(collection_id)

                    # it considers single data that is adjacent to other catalogRefs in main catalog as a single collection
                    elif "dataset" in str(c) and catalogRef_list != []:
                        branches_main.append(
                            url
                            + "?dataset="
                            + c.get("ID").replace("html", "xml")
                        )

                        collection_id = utils.replacement_func(
                            url
                            + "?dataset="
                            + c.get("ID")
                            + " SingleDataset".replace("html", "xml")
                        )
                        self.logger.info(collection_id)

                # when it harvests a dataset without any catalogRef and sub-dataset
                if (
                    dataset_list != []
                    and catalogRef_list == []
                    and url == self.xml_url_catalog
                ):
                    branches_main.append(utils.html2xml(url))
                    collection_id = utils.replacement_func(
                        url + " Collection".replace("html", "xml")
                    )
                    self.logger.info(collection_id)

            if "dataset" in str(child) and self.aggregated_dataset == True:
                branches_main.append(utils.html2xml(url))

                collection_id = utils.replacement_func(
                    url + " Aggregated".replace("html", "xml")
                )
                self.logger.info(collection_id)
                # creation of collection
        # Finding all data in datasets to create items

        data_main = []
        for e in branches_main:
            try:
                url_stat = requests.get(e, None, verify=False)
                content = url_stat.text.encode("utf-8")

            except BaseException:
                continue
            data_main.append(content)
        # A loop through the nested datasets
        for i, d in enumerate(data_main):
            for dataset in self.collection_ids(branches_main[i], d):
                yield dataset
