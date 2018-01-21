from sanic import response
from utils.server import check_request, get_index, manic_port
from manic.app import Manic

'''
Manic - hella fast mapped memory lookup server  v 0.00aa
(c) 2018 - kaotik.io - All Rights Reserved

uses python asynch methods in Sanic
'''


app = Manic()

@app.route("/")
async def test(request):
    pl = "{'manic':'I am a teapot'}"
    return response.json(pl, status=418)


@app.route("/f", methods=['GET'])
async def find(request):

    # check to make sure the query is formed properly
    # get the index name and search term
    idx, st = check_request(request)

    # select the index
    s_idx = get_index(idx, app._indices)

    # lookup the search term
    return app.find(s_idx, st)

if __name__ == "__main__":

    app.start(host="0.0.0.0", port=manic_port(app._config))



