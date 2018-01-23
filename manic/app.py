from sanic import Sanic, response
from utils.server import logging_level, manic_setup, mapped_filename, scream, plain_response, \
    no_result, parsed_response, is_parsed_response
from utils.data import create, index, _find, load_memfile_configs
from manic.exceptions import ManicIndexingError
import logging


class Manic(Sanic):

    def __init__(self):

        super(Manic, self).__init__()

        # logfile TODO - make this work
      #  self._log = logging.getLogger("Manic")
      #  self._log.setLevel(logging_level(self._config["server"]["loglevel"]))

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
        scream()

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
                if name in self._mmm:
                    msg = "column-index names must be unique within and across files"
                    raise ManicIndexingError(msg)
                
                self._mmm[name] = (idx, mm, cfg)

        print("host: {} port: {}".format(host, port))
        super(Manic, self).run(host="0.0.0.0", port=5216)


    def find(self, idx, st):
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

        if is_parsed_response(cfg):
            return response.text(parsed_response(resp, exec_time, cfg), status=200)
        return response.text(plain_response(resp, exec_time), status=200)