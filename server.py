from utils.server import check_request
from manic.app import Manic
from utils.helpers import teapot
import config

'''
Manic - hella fast mapped memory lookup server  v 0.1
(c) 2018 - kaotik.io - All Rights Reserved

uses python async methods in Sanic
'''

app = Manic()


@app.route("/")
async def test(request):
    return teapot()


@app.route("/f", methods=['GET'])
async def find(request):

    # check to make sure the query is formed properly
    # get the index name and search term
    idx, st = check_request(request)

    # lookup the search term
    return app.m_find(idx, st)


# start
app.start(host=config.HOST, port=config.PORT)



