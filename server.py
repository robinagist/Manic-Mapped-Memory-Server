from sanic import Sanic, response
from utils.server import server_config, check_request, logging_level, get_index, no_result
from utils.data import create, index, define_columns_using_delimiter, define_lastline_newline, _find
import logging

'''
Manic - hella fast mapped memory lookup server  v 0.00aa
(c) 2018 - kaotik.io - All Rights Reserved

uses python asynch methods in Sanic
'''

# get the server configuration
_config = server_config()

# logfile TODO - make this work
_log = logging.getLogger("Manic")
_log.setLevel(logging_level(_config["server"]["loglevel"]))

# where the created indices are stored
_indices = dict()
# memory mapped file reference
_mm = None

app = Sanic()

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
    s_idx = get_index(idx, _indices)

    # lookup the search term
    resp, exec_time = _find(_mm, s_idx, st)

    if not resp:
        return response.json(no_result(st, exec_time), 404)

    pl = dict()
    pl["result"] = resp
    pl["lookup-time-ms"] = exec_time

    return response.text(pl, status=200)


if __name__ == "__main__":

    # verify and validate the score file
    print("loading file into memory map...")

    # load score file into memory map
    _mm = create(_config["memmap"]["filepath"])

    # define the column layout and indexing
    cols = _config["memmap"]["columns"]
    delimiter = _config["memmap"]["delimiter"]
    cis = define_columns_using_delimiter(cols, delimiter)
    define_lastline_newline(cis, _config["memmap"]["llnf"])

    # create hashed lookups for file
    print("creating indices...")
    _indices = index(_mm, cis)

    app.run(host="0.0.0.0", port=8000)



