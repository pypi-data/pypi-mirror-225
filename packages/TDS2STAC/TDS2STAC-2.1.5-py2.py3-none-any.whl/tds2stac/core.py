import re
import traceback
from datetime import datetime

import pytz

from . import constants, utils


def iso_core(input_xml):
    """A function for looping over the subtags in ISO XML files"""
    for tag in input_xml:
        # when a tag has subtags, then `tag.text` is not `None` or `whitespace`.
        if tag.text is None or tag.text.isspace():
            return iso_core(tag)
        else:
            return tag.text


def wms_core(input_xml, var_name):
    """A core function that acts differently for each tag in WMS XML files."""
    # Each `Layer` tag in WMS that has a `queryable` attribute contains the variables and dimensions as subtags.
    if (var_name == "keyword" or var_name == "var_dims") and input_xml.get(
        "queryable"
    ) is not None:
        dim_list = []
        for attr in input_xml:
            if (
                attr.tag == "{%s}BoundingBox" % constants.wms
                and attr.get("minx") is not None
                and attr.get("maxx") is not None
            ):
                dim_list.append("lon")
            if (
                attr.tag == "{%s}BoundingBox" % constants.wms
                and attr.get("minx") is not None
                and attr.get("minx") is not None
            ):
                dim_list.append("lat")
            if (
                attr.tag == "{%s}Dimension" % constants.wms
                and attr.get("name") == "time"
            ):
                dim_list.append("time")
        return dim_list

    # The `Name` subtag of `Layer` tag of a WMS XML file contains the variable names of a dataset.
    elif var_name == "var_lists" and input_xml.get("queryable") is not None:
        for subtag in input_xml:
            if subtag.tag == "{%s}Name" % constants.wms:
                return subtag.text
    # The `Title` subtag of `Layer` tag of a WMS XML file contains the variable names of a dataset.
    elif var_name == "var_descs" and input_xml.get("queryable") is not None:
        for i in input_xml:
            if i.tag == "{%s}Title" % constants.wms:
                return i.text
    # DateTime is contained within the `Dimension` tag and need to be ordered in WMS XML file.
    elif var_name == "time_start":
        all_params = re.split("/|,|\n", input_xml.text.replace(" ", ""))
        print(all_params)
        try:
            datetime_formated = [
                datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                    tzinfo=pytz.utc
                )
                for x in all_params
                if "T" in x and "Z" in x
            ]
        except:
            print(traceback.format_exc())
            datetime_formated = [
                datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").replace(
                    tzinfo=pytz.utc
                )
                for x in all_params
                if "T" in x and "Z" in x
            ]

        return min(datetime_formated).strftime("%Y-%m-%dT%H:%M:%SZ")
    elif var_name == "time_end":
        all_params = re.split("/|,|\n", input_xml.text.replace(" ", ""))
        try:
            # Only when datetime contains microsecond
            datetime_formated = [
                datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                    tzinfo=pytz.utc
                )
                for x in all_params
                if "T" in x and "Z" in x
            ]
        except:
            # Only when datetime contains microsecond
            datetime_formated = [
                datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").replace(
                    tzinfo=pytz.utc
                )
                for x in all_params
                if "T" in x and "Z" in x
            ]
        return max(datetime_formated).strftime("%Y-%m-%dT%H:%M:%SZ")
    # For non-list variables
    elif (
        var_name == "long_min"
        or var_name == "long_max"
        or var_name == "lat_min"
        or var_name == "lat_max"
    ):
        return input_xml.text


def ncml_core(input_xml, var_name):
    """A core function to acts different over the tags in ncml XML files"""
    # The variable tags in NcML XML file with an empty name and shape cannot be referred to as variable in NcML files.
    if (
        var_name == "var_lists"
        and input_xml.get("name") is not None
        and not input_xml.get("name").isspace()
        and input_xml.get("shape") is not None
        and not input_xml.get("shape") == ""
    ):
        return input_xml.get("name")
    # The dimension tag of a NcML XML file contains the dimensions of a NetCDF file.
    elif (
        var_name == "var_dims"
        and input_xml.get("name") is not None
        and not input_xml.get("name").isspace()
    ):
        return input_xml.get("name")
    # The `long_name` or `standard_name` attribute of the variable subtags describes each variable.
    elif (
        var_name == "var_descs"
        and input_xml.get("shape") is not None
        and not input_xml.get("shape") == ""
    ):
        name_box = [i.get("name") for i in input_xml]
        shape_box = [i.get("value") for i in input_xml]
        # Another condition should be added for `standard_name` attribute!!!!
        if "long_name" in name_box:
            return shape_box[name_box.index("long_name")]
        else:
            return "No description available"
    # Each variable's dimensions are contained in the shape attribute of the variable tag.
    elif (
        var_name == "keyword"
        and input_xml.get("shape") is not None
        and not input_xml.get("shape") == ""
    ):
        return [input_xml.get("shape").split()]
    # All other tags are returned as they are in the XML file as far as the value attributes are not empty.
    elif (
        input_xml.get("value") is not None
        and not input_xml.get("value").isspace()
    ):
        return input_xml.get("value")


def auto_switch_harvester(input_xml, web_servicess, var_name, types):
    """A function that acts differently for each tag in NcML XML files."""
    # a dictionary for selecting the right function for each webservice in TDS.
    if web_servicess == "iso":
        webservice_selector_iso = dict(
            iso={
                "var": iso_core(input_xml)
                if input_xml.text is None or input_xml.text.isspace()
                else input_xml.text,
            },
        )
        # when the variable is not available (None) in the ISO XML file
        if webservice_selector_iso["iso"][types] is None:
            webservice_selector_iso["iso"][types] = "No info available"
        # when the variable is available in the ISO XML file
        reference_selector = {
            constants.webservices_constants[web_servicess][
                var_name
            ]: webservice_selector_iso[web_servicess][types]
        }

    if web_servicess == "ncml":
        webservice_selector_ncml = dict(
            ncml={
                "var": ncml_core(input_xml, var_name),
            },
        )
        # when the variable is available in the ISO XML file
        reference_selector = {
            constants.webservices_constants[web_servicess][
                var_name
            ]: webservice_selector_ncml[web_servicess][types]
        }

    if web_servicess == "wms":
        webservice_selector_wms = dict(
            wms={
                "var": wms_core(input_xml, var_name),
            },
        )
        # when the variable is available in the ISO XML file
        reference_selector = {
            constants.webservices_constants[web_servicess][
                var_name
            ]: webservice_selector_wms[web_servicess][types]
        }

    return reference_selector.get(
        constants.webservices_constants[web_servicess][var_name],
        "No info available",
    )


def harvesting_core(tags, ws, harvesting_vars):
    """A Core function for harvesting the various tryps of varialbe e.g list and non-list variables."""
    for attrs in constants.constant_list:
        if (
            utils.xml_tag_finder(
                tags,
                ws,
                attrs,
            )
            == constants.webservices_constants[ws][attrs]
        ):
            harvesting_vars[attrs] = auto_switch_harvester(
                tags,
                ws,
                attrs,
                "var",
            )
    for attrs in constants.append_list:
        if (
            utils.xml_tag_finder(
                tags,
                ws,
                attrs,
            )
            == constants.webservices_constants[ws][attrs]
        ):
            harvesting_vars[attrs].append(
                auto_switch_harvester(
                    tags,
                    ws,
                    attrs,
                    "var",
                )
            )
