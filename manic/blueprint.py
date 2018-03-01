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
@bp.route("/admin/files", methods=['GET'])
async def list_memmapped_files(request):
    '''
    list the memmapped files
    :param request:
    :return:
    '''

    return get_mappedfile_configs()

@bp.route("/admin/files", methods=['POST'])
async def create_memmapped_file(request):
    '''
    creates a memmapped file configuration
    :param request:
    :return:


    request data looks like:
    {"

    '''

    # extract the mapped file configuration from the request

    pass

@bp.route("/admin/files", methods=['DELETE'])
async def delete_memmapped_file(request):
    '''
    delete a memmapped file configuration
    :param request:
    :return:
    '''
    pass

@bp.route("/admin/restart", methods=["POST"])
async def restart(request):
    '''
    restarts the server
    :param request:
    :return:
    '''
    pass




