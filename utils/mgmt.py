from utils.data import load_memfile_configs
from utils.server import plain_response
from sanic import response




def get_mappedfile_configs():
    cfgs = load_memfile_configs()
    return response.json(plain_response(cfgs, 0), status=200)

def created_mapped_file():
    #
    pass

