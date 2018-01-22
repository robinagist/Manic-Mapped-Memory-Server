import json
import logging
from sanic.exceptions import SanicException
from utils import data
import config


# helper - returns the mappped file path from the app configuration
def mapped_filename(cfg):
    fn = cfg["filepath"]
    fdir = cfg["mmname"]
    basedir = config.BASE_PATH
    memfilesdir = config.MEMFILES_DIR
    return "{}/{}/{}/{}".format(basedir, memfilesdir, fdir, fn)


# helper - returns the index/column config
def index_config(config):
    return config["memmap"]["column_def"]


# helper - returns the server port number from config
def manic_port(config):
    return config["server"]["port"]


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
        # _log.warning("malformed query: index {} not found".format(idx))
        raise SanicException(msg, 400)
    return indices[idx]


# cannot find the search term helper
def no_result(st, exec_time):
    pl = dict()
    pl["error"] = "unable to find {}".format(st)
    pl["lookup-time-ms"] = exec_time
    return pl

# format a response helper
def plain_response(resp, exec_time):
    pl = dict()
    pl["result"] = resp
    pl["rows-returned"] = len(resp)
    pl["lookup-time-ms"] = exec_time
    return pl


# get the column names
def get_column_names(config):
    names = []
    cols = config["indexes"]
    for col in cols:
        n = col["name"]
        names.append(n)
    return names

# returns the format preference
def is_parsed_response(config):
    if config["result-format"] == "PARSE":
        return True
    return False

# format a parsed response helper
def parsed_response(resp, exec_time, config):
    pl = dict()
    rl = list()
    cols = get_column_names(config)
    for line in resp:
        cc = 0
        d = dict()
        l = line.strip().split(',')
        for col in cols:
            d[col] = l[cc]
            cc += 1
        rl.append(d)
    pl["result"] = rl

    pl["rows-returned"] = len(resp)
    pl['lookup-time-ms'] = exec_time
    return pl

# sets up the configuration for indexing and searching
def manic_setup(config):
    cols = config["indexes"]
    delimiter = config["delimiter"]
    cis = data.define_columns_using_delimiter(cols, delimiter)
    data.define_lastline_newline(cis, config["llnf"])
    return cis

# helper app startup blurb
def scream():
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