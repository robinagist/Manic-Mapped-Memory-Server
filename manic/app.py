from sanic import Sanic, response
from utils.server import server_config, logging_level, manic_setup, mapped_filename, scream, plain_response, \
    no_result, parsed_response, is_parsed_response, get_index
from utils.verify import verify_file, verify_filename, verify_errors
from utils.data import create, index, _find, load_memfile_configs, mf_index
import logging
import time


class Manic(Sanic):

    def __init__(self):

        super(Manic, self).__init__()

        # server configuration
        self._config = server_config()

        # logfile TODO - make this work
        self._log = logging.getLogger("Manic")
        self._log.setLevel(logging_level(self._config["server"]["loglevel"]))

        # where the created single file indices are stored
        self._indices = dict()

        # multifile indices
        self._indexes = dict()

        # memory mapped file reference
        self._mm = None

        # multiple mapped files reference
        self._mmm = dict()

    def start(self, host, port):
        # intro blurb
        scream(self._config)

        # verify and validate the score file
   #     print("verifying file against hash provided by originator")
   #     errors, bypassed = verify_file(mapped_filename(self._config), verify_filename(self._config), bypass=True)

   #     if errors:
   #         verify_errors(errors)

   #     print("bypass verification is set to `True` - file not verified") if bypassed else print("verified")
   #     print("loading files into memory maps...")

        # load memfiles configurations
        cfgs = load_memfile_configs()
        # load files into memory maps
        for cfg in cfgs:
            # maps the file to memory
            mm = create(mapped_filename(cfg))
            # sets up the parsing configuration
            setup_c = manic_setup(cfg)
            indexes = index(mm, setup_c)
            # add lookup for index to memmap
            for name, idx in indexes.items():
                self._mmm[name] = (idx, mm, cfg)

        print("host: {} port: {}".format(host, port))
        super(Manic, self).run(host="0.0.0.0", port=5216)

    def find(self, idx, st):

        s_idx = get_index(idx, self._indices)
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
            return response.text(parsed_response(resp, exec_time, self._config), status=200)
        return response.text(plain_response(resp, exec_time), status=200)

    def m_find(self, idx, st):
        '''
        multifile find
        :param idx:
        :param st:
        :return:
        '''
        # s_idx = get_index(idx, self._indices)
        if idx not in self._mmm:
            msg = "index column `{}` not found".format(idx)
            return response.text(plain_response(msg, 0), status=400)

        s_idx = self._mmm[idx][0]
        mm = self._mmm[idx][1]
        cfg = self._mmm[idx][2]

        resp, exec_time = _find(mm, s_idx, st)
        # if index is empty, that means column was marked for non-indexing
        if resp == 0 and exec_time == 0:
            msg = "column not indexed and is not searchable"
            return response.text(plain_response(msg, exec_time), status=400)

        # if search term not found on selected index
        if not resp:
            return response.text(no_result(st, exec_time), status=404)

        # use response helper to send JSON reply
 #       if is_parsed_response(self._config):
 #           return response.text(parsed_response(resp, exec_time, self._config), status=200)
        return response.text(plain_response(resp, exec_time), status=200)