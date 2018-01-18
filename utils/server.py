import json
import logging
from sanic.exceptions import SanicException
from utils import data

def server_config():
 #   try:
    with open('/Users/robin/PycharmProjects/manic/config.json') as configfile:
        data = json.load(configfile)
#    except:
#        raise Exception("missing configuration file")
    return data

# helper - returns the mappped file path from the app configuration
def mapped_filename(config):
    return config["memmap"]["filepath"]


def check_request(req):
    req_args = req.raw_args
    if "idx" not in req_args:
        raise SanicException('missing index parameter `idx`', 400)
    if "st" not in req_args:
        raise SanicException('missing search parameter `st`', 400)
    return req_args["idx"], req_args["st"]


def get_index(idx, indices):
    if idx not in indices:
        msg = "{{'manic':'malformed query (index {} not found)' }}".format(idx)
        _log.warning("malformed query: index {} not found".format(idx))
        raise SanicException(msg, 400)
    return indices[idx]


# cannot find the search term helper
def no_result(st, exec_time):
    pl = dict()
    pl["error"] = "unable to find {}".format(st)
    pl["lookup-time-ms"] = "lookup-time-ms {}".format(exec_time)
    return pl

# format a response helper
def plain_response(resp, exec_time):
    pl = dict()
    pl["result"] = resp
    pl["lookup-time-ms"] = exec_time
    return pl

# sets up the configuration for indexing and searching
def manic_setup(config):
    cols = config["memmap"]["columns"]
    delimiter = config["memmap"]["delimiter"]
    cis = data.define_columns_using_delimiter(cols, delimiter)
    data.define_lastline_newline(cis, config["memmap"]["llnf"])
    return cis

# helper app startup blurb
def scream(config=None):
    print()
    print("Manic Fast Mapped Memory Server 0.0a")
    print("(c) 2018 - kaotik.io - all rights reserved")
    print("released under the terms and conditions of the MIT Public License")
    print()


def logging_level(manic_level):
    if manic_level == "WARN":
        return logging.WARN
    if manic_level == "INFO":
        return logging.INFO
    if manic_level == "DEBUG":
        return logging.DEBUG