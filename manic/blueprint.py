from utils.server import check_request
from utils.helpers import teapot
from utils.mgmt import get_mappedfile_configs
import config
from sanic import Blueprint

'''
Manic - hella fast mapped memory lookup server
(c) 2018 - kaotik.io - All Rights Reserved

runs on top of Sanic async framework
'''

bp = Blueprint('manic')


@bp.route("/")
async def test(request):
    return teapot()


@bp.route("/f", methods=['GET'])
async def find(request):

    # check to make sure the query is formed properly
    # get the index name and search term
    idx, st = check_request(request)
    # lookup the search term
    return request.app.find(idx, st)

# file management methods
# TODO authentication - session mgmt
@bp.route("/files", methods=['GET'])
async def list_files(request):
    '''
    list the memmapped files
    :param request:
    :return:
    '''

    return get_mappedfile_configs()






