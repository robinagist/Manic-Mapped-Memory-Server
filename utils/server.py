import configparser
import json
import logging
from sanic.exceptions import SanicException

from sanic import Sanic, response, request
# from sanic.response import json

def server_config():
 #   try:
    with open('/Users/robin/PycharmProjects/manic/config.json') as configfile:
        data = json.load(configfile)
#    except:
#        raise Exception("missing configuration file")
    return data


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

def no_result(st, exec_time):
    return "{{'manic':'unable to find {}', 'lookup_time_milliseconds':{}}}".format(st, exec_time)


def logging_level(manic_level):
    if manic_level == "WARN":
        return logging.WARN
    if manic_level == "INFO":
        return logging.INFO
    if manic_level == "DEBUG":
        return logging.DEBUG