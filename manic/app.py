from sanic import Sanic, response
from utils.server import server_config, logging_level, manic_setup, mapped_filename ,scream, plain_response, no_result, parsed_response, is_parsed_response
from utils.verify import verify_file, verify_filename, verify_errors
from utils.data import create, index, _find
import logging




class Manic(Sanic):

    def __init__(self):

        super(Manic, self).__init__()

        # server configuration
        self._config = server_config()

        # logfile TODO - make this work
        self._log = logging.getLogger("Manic")
        self._log.setLevel(logging_level(self._config["server"]["loglevel"]))

        # where the created indices are stored
        self._indices = dict()

        # memory mapped file reference
        self._mm = None

    def start(self, host, port):
        # intro blurb
        scream(self._config)

        # verify and validate the score file
        print("verifying file against hash provided by originator")
        errors, bypassed = verify_file(mapped_filename(self._config), verify_filename(self._config), bypass=True)

        if errors:
            verify_errors(errors)

        print("bypass verification is set to `True` - file not verified") if bypassed else print("verified")
        print("loading file into memory map...")
        # load score file into memory map
        self._mm = create(mapped_filename(self._config))

        # define the column layout and indexing
        setup_c = manic_setup(self._config)

        # create hashed lookups for file
        print("creating indices...")
        self._indices = index(self._mm, setup_c)
        print("host: {} port: {}".format(host, port))
        super(Manic, self).run(host="0.0.0.0", port=5216)

    def find(self, s_idx, st ):
        resp, exec_time = _find(self._mm, s_idx, st)
        # if index is empty, that means column was marked for non-indexing
        if resp == 0 and exec_time == 0:
            msg = "column not indexed and is not searchable"
            return response.text(plain_response(msg, exec_time), status=400)

        # if search term not found on selected index
        if not resp:
            return response.text(no_result(st, exec_time), status=404)

        # use response helper to send JSON reply
        if is_parsed_response(self._config):
            print("parsed response")
            return response.text(parsed_response(resp, exec_time, self._config), status=200)
        return response.text(plain_response(resp, exec_time), status=200)

