
from sanic import Sanic, response
from sanic.response import json
from sanic.exceptions import SanicException

from utils.utils import start_clock, end_clock
from utils.server import server_config, check_request
from utils.data import create, index, define_columns_using_delimiter, define_lastline_newline, _find


import json, time
'''
Manic - hella fast mapped memory lookup server  v 0.00aa
(c) 2018 - kaotik.io - All Rights Reserved

uses python asynch methods in Sanic
'''

# get the server configuration
_config = server_config()

# memory mapped file reference
_mm = None

# where the created indices are stored
_indices = dict()

app = Sanic()

@app.route("/")
async def test(request):
    pl = "{'manic':'I am a teapot'}"
    return response.json(pl, status=418)


@app.route("/f", methods=['GET'])
async def find(request):

    errors = check_request(request)
    if errors:
        return response.text(errors, 400)

    idx = request.raw_args["idx"]
    st = request.raw_args["st"]

    if idx not in _indices:
        msg = "{{'manic':'malformed query (index {} not found)' }}".format(idx)
        return response.json(msg, 400)

    s_idx = _indices[idx]
    resp, exec_time = _find(_mm, s_idx, st)

    if not resp:
        msg = "{{'manic':'unable to find {}', 'lookup_time_milliseconds':{}}}".format(st, exec_time)
        return response.json(msg, 404)

    pl = "{{'result':'{}','lookup-time-milliseconds':'{}'}}".format(resp, exec_time)

    return response.json(pl, status=200)


if __name__ == "__main__":
    # TODO - extract

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



