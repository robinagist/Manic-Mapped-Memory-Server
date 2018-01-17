
from sanic import Sanic, response
from sanic.response import json
from sanic.exceptions import SanicException

from utils.utils import start_clock, end_clock
from utils.server import server_config, check_required
from utils.data import find, create, index, define_columns_using_delimiter, define_lastline_newline


import json, time
'''
Manic - hella fast mapped memory lookup server

v 0.00aa

(c) 2018 - kaotik.io - All Rights Reserved
THIS CODE NOT FOR DISTRIBUTION

uses python asynch methods in Sanic
'''

# get the server configuration
config = server_config()

# hand lookup index
_h = dict()
# hashed hand lookup index
_hh = dict()
# hashed hand score lookup index
_hhs = dict()

# memory mapped file reference
_mm = None
_indices = dict()

app = Sanic()

@app.route("/")
async def test(request):
    pl = "{'manic':'I am a teapot'}"
    return response.json(pl, status=418)


@app.route("/f", methods=['GET'])
async def get_score_by_hand(request):

    req_args = request.raw_args
    idx, st = check_required(req_args)

    if not idx or not st:
        msg = st
        return response.json(msg, 400)

    s_idx = None
    if idx not in _indices:
        msg = "{{'manic':'malformed query (index {} not found)' }}".format(idx)
        return response.json(msg, 400)
    s_idx = _indices[s_idx]

    begin_request_time = start_clock()
    # returns the score for the hand
    resp = find(_mm, s_idx, st)
    exec_time = end_clock(begin_request_time)

    if not resp:
        msg = "{{'manic':'unable to find {}', 'search_time_milliseconds':{}}}".format(st, exec_time)
        return response.json(msg, 404)

    pl = "{{'result':'{}','lookup-time-milliseconds':'{}'}}".format(resp, exec_time)

    return response.json(pl, status=200)


if __name__ == "__main__":

    filename = "/Users/robin/poker/test-scores-file.txt"

    # verify and validate the score file
    print("loading file into memory map...")

    # load score file into memory map
    _mm = create(filename)

    # define the column layout and indexing
    cols = ["hand", None, "hh", "hhs"]
    cis = define_columns_using_delimiter(cols, ",")
    define_lastline_newline(cis, n=True)

    # create hashed lookups for file
    print("creating indices...")
    _indices = index(_mm, cis)

    app.run(host="0.0.0.0", port=8000)



