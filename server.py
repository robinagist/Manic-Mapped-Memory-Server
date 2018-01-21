from utils.server import check_request
from manic.app import Manic
from utils.helpers import teapot

'''
Manic - hella fast mapped memory lookup server  v 0.1
(c) 2018 - kaotik.io - All Rights Reserved

uses python asynch methods in Sanic
'''

app = Manic()

@app.route("/t")
async def test(request):
    return teapot()

@app.route("/f", methods=['GET'])
async def find(request):

    # check to make sure the query is formed properly
    # get the index name and search term
    idx, st = check_request(request)

    # lookup the search term
    return app.find(idx, st)

if __name__ == "__main__":

    app.start(host="0.0.0.0", port=5216)



