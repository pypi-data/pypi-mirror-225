import os
from urllib import parse as urlparse

import requests


def replacement_func(url):
    """A function for making a an id from catalog URL for collections"""
    splitted_arr = urlparse.urlsplit(url)
    trans_dict_path = {"%": "", "/catalog.xml": "", "/thredds/": "", "/": " "}
    path_ = splitted_arr.path
    query_ = splitted_arr.query
    for k, v in trans_dict_path.items():
        temp = path_.split(k)
        path_ = v.join(temp)
    if splitted_arr.query != "":
        trans_dict_query = {"=": " ", "?": " ", "/": " "}
        for k, v in trans_dict_query.items():
            temp = query_.split(k)
            query_ = v.join(temp)
        replaced_url = path_.replace(".xml", "") + " " + query_
        trans_dict_replaced = {".nc": "", "-": " ", "_": " "}
        for k, v in trans_dict_replaced.items():
            temp = replaced_url.split(k)
            replaced_url = v.join(temp)
    else:
        replaced_url = path_
        trans_dict_replaced = {".xml": "", ".nc": "", "-": " ", "_": " "}
        for k, v in trans_dict_replaced.items():
            temp = replaced_url.split(k)
            replaced_url = v.join(temp)
    return replaced_url.title()


def html2xml(url):
    """A function for making a an xml URL from html URL"""
    u = urlparse.urlsplit(url)
    path, extesion = os.path.splitext(u.path)
    if extesion == ".html":
        u = urlparse.urlsplit(url.replace(".html", ".xml"))
    return u.geturl()


def xml2html(url):
    """A function for making a an html URL from xml URL"""
    u = urlparse.urlsplit(url)
    path, extesion = os.path.splitext(u.path)
    if extesion == ".xml":
        u = urlparse.urlsplit(url.replace(".xml", ".html"))
    return u.geturl()


def get_xml(url):
    """A function for getting XML content from url"""
    try:
        xml_url = requests.get(url, None, verify=False)
        xml = xml_url.text.encode("utf-8")
    except BaseException:
        pass
    return xml


def references_urls(url, additional):
    splitted_arr = urlparse.urlsplit(url)
    common_url = str(splitted_arr.scheme) + "://" + str(splitted_arr.netloc)
    wihtout_catalog_xml = urlparse.urljoin(
        common_url, os.path.split(splitted_arr.path)[0]
    )
    if not additional:
        final_url = url
    elif additional[0] == "h":
        # finding http or https
        final_url = additional
    elif additional[0] == "/":
        # Absolute paths
        final_url = urlparse.urljoin(common_url, additional)
    else:
        # Relative paths.
        final_url = wihtout_catalog_xml + "/" + additional
    return final_url


def xml_processing(catalog):
    """A function for getting out XML details of a catalog URL"""
    catalog_xml = html2xml(catalog)
    catalog_id = replacement_func(catalog_xml)
    xml_final = get_xml(catalog_xml)
    return catalog_xml, catalog_id, xml_final


def xml_tag_name_ncml(input_xml, var_name):
    """A function for finding the tag names in NcML XML files"""

    # A list for recognizign the exceptions.
    # This list contains variable's name with same `input_xml.tag` and different `var_name`s
    exception_list = ["var_lists", "var_dims", "var_descs", "keyword"]

    if var_name in exception_list:
        return input_xml.tag + "_" + var_name
    else:
        return str(input_xml.get("name")) + "_" + var_name


def xml_tag_finder(input_xml, web_service, var_name):
    """A function for finding the tag names in all TDS webservices"""

    tag_finder_dict = {
        "iso": input_xml.tag + "_" + var_name,
        "ncml": xml_tag_name_ncml(input_xml, var_name),
        "wms": input_xml.tag + "_" + var_name,
    }

    return tag_finder_dict.get(
        web_service,
    )
