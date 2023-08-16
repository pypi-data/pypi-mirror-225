unidata = "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0"
w3 = "http://www.w3.org/1999/xlink"
iso_gmd = "http://www.isotc211.org/2005/gmd"
iso_gco = "http://www.isotc211.org/2005/gco"
iso_gml = "http://www.opengis.net/gml/3.2"
global_bounding_box = [-360, -90, 0, 90]
No_inf = "No information"
ncml = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"
wms = "http://www.opengis.net/wms"
# a list of parameters to be not used in 'aName' parameter in iso webservice and 'dimension' and 'variable' parameters in ncML webservice
avoided_list = ["time_bnds", "bnds", "ens"]
# a list of parameters to be used in 'keyword' parameter in iso webservice
allowed_list = [
    "time",
    "lat",
    "latitude",
    "lon",
    "longitude",
    "long",
    "time_bnds",
    "bnds",
]
# a list of parameters to avoid use of them in final item
avoided_formats = [
    "float",
    "double",
    "int",
    "time_bnds",
    "bnds",
    "ens",
    "String",
    "short",
]
# Deafult value for having a bounding box for time-series data.
epilon = 0.000001


# webservice types that TDS2STAC supports
webservices_list = ["ncml", "wms", "iso"]
# List of array value attributes in `auto_switch_harvester`
append_list = ["keyword", "var_lists", "var_descs", "var_dims"]
# List of single value attributes in `auto_switch_harvester`
constant_list = [
    "long_min",
    "long_max",
    "lat_min",
    "lat_max",
    "time_start",
    "time_end",
]
# In the loop of 'auto_switch_harvester', criteria for locating the correct tag.
webservices_constants = dict(
    iso={
        "long_min": "{%s}westBoundLongitude_long_min" % iso_gmd,
        "long_max": "{%s}eastBoundLongitude_long_max" % iso_gmd,
        "lat_min": "{%s}southBoundLatitude_lat_min" % iso_gmd,
        "lat_max": "{%s}northBoundLatitude_lat_max" % iso_gmd,
        "keyword": "{%s}dimensionName_keyword" % iso_gmd,
        "var_lists": "{%s}MemberName_var_lists" % iso_gco,
        "var_descs": "{%s}descriptor_var_descs" % iso_gmd,
        "var_dims": "{%s}dimensionName_var_dims" % iso_gmd,
        "time_start": "{%s}beginPosition_time_start" % iso_gml,
        "time_end": "{%s}endPosition_time_end" % iso_gml,
    },
    ncml={
        "long_min": "geospatial_lon_min_long_min",
        "long_max": "geospatial_lon_max_long_max",
        "lat_min": "geospatial_lat_min_lat_min",
        "lat_max": "geospatial_lat_max_lat_max",
        "keyword": "{%s}variable_keyword" % ncml,
        "var_lists": "{%s}variable_var_lists" % ncml,
        "var_descs": "{%s}variable_var_descs" % ncml,
        "var_dims": "{%s}dimension_var_dims" % ncml,
        "time_start": "time_coverage_start_time_start",
        "time_end": "time_coverage_end_time_end",
    },
    wms={
        "long_min": "{%s}westBoundLongitude_long_min" % wms,
        "long_max": "{%s}eastBoundLongitude_long_max" % wms,
        "lat_min": "{%s}southBoundLatitude_lat_min" % wms,
        "lat_max": "{%s}northBoundLatitude_lat_max" % wms,
        "keyword": "{%s}Layer_keyword" % wms,
        "var_lists": "{%s}Layer_var_lists" % wms,
        "var_descs": "{%s}Layer_var_descs" % wms,
        "var_dims": "{%s}Layer_var_dims" % wms,
        "time_start": "{%s}Dimension_time_start" % wms,
        "time_end": "{%s}Dimension_time_end" % wms,
    },
)
