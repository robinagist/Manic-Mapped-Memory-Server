import configparser
from sanic import Sanic, response
from sanic.response import json

def server_config():
    config = configparser.ConfigParser()
    cf = "manic.conf"

    try:
        config.read(cf)
        return config
    except:
        pass


def check_required(req_args):
    if "idx" not in req_args:
        msg = "{{'manic':'malformed query (missing index 'idx')' }}"
        return False, msg

    if "st" not in req_args:
        msg = "{{'manic':'malformed query (missing search term 'st')' }}"
        return False, msg

    # find the right index
    idx = req_args["idx"]
    st = req_args["st"]

    return idx, st