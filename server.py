from sanic import Sanic, response
from utils.server import server_config, check_request, logging_level, get_index, no_result, \
    plain_response, manic_setup, mapped_filename ,scream, manic_port
from utils.data import create, index, _find
from utils.verify import verify_file, verify_filename, verify_errors
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

    # if index is empty, that means column was marked for non-indexing
    if resp == 0 and exec_time == 0:
        msg = "column not indexed and is not searchable"
        return response.text(plain_response(msg, exec_time), status=400)

    # if search term not found on selected index
    if not resp:
        return response.text(no_result(st, exec_time), status=404)

    # use response helper to send JSON reply
    return response.text(plain_response(resp, exec_time), status=200)


if __name__ == "__main__":

    # intro blurb
    scream(_config)

    # verify and validate the score file
    print("verifying file against hash provided by originator")
    errors, bypassed = verify_file(mapped_filename(_config), verify_filename(_config), bypass=True)

    if errors:
        verify_errors(errors)
        
    print("bypass verification is set to True - file not verified") if bypassed else print("verified")

    print("loading file into memory map...")
    # load score file into memory map
    _mm = create(mapped_filename(_config))

    # define the column layout and indexing
    setup_c = manic_setup(_config)

    # create hashed lookups for file
    print("creating indices...")
    _indices = index(_mm, setup_c)

    app.run(host="0.0.0.0", port=manic_port(_config))



