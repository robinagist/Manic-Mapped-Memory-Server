from utils.server import check_request
from utils.helpers import teapot
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


# app.start(host=config.HOST, port=config.PORT)



