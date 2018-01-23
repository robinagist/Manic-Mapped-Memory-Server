from utils.server import check_request
from manic.app import Manic
from utils.helpers import teapot
import config

'''
Manic - hella fast mapped memory lookup server
(c) 2018 - kaotik.io - All Rights Reserved

runs on top of Sanic async framework
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
    return app.find(idx, st)


app.start(host=config.HOST, port=config.PORT)



