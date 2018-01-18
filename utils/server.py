import configparser
import json

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
    errors = list()
    if "idx" not in req_args:
        errors.append('missing index parameter `idx`')
    if "st" not in req_args:
        errors.append('missing search parameter `st`')
    if errors:
        error_d = dict()
        error_d['errors'] = errors
        return json.dumps(error_d, ensure_ascii=False)
    return errors
