from sanic import Sanic, response
from utils.server import manic_setup, mapped_filename, scream, plain_response, \
    no_result, parsed_response, is_parsed_response
from utils.data import create, index, _find, load_memfile_configs, check_memfile_configs
import config as cfg


class Manic(Sanic):

    def __init__(self):

        super(Manic, self).__init__()

        # set up server configuration
        if cfg.KEEP_ALIVE == 0:
            self.config.KEEP_ALIVE_TIMEOUT = 0
            self.config.KEEP_ALIVE = False
        else:
            self.config.KEEP_ALIVE = True
            self.config.KEEP_ALIVE_TIMEOUT = cfg.KEEP_ALIVE

        # multiple mapped files reference
        self._mmm = dict()

    def start(self, host, port):
        # intro blurb
        scream()

        # load memfiles configurations
        cfgs = load_memfile_configs()

        # make sure there are no problems in the configs
        # error raised if a problem
        check_memfile_configs(cfgs)

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

        super(Manic, self).run(host="0.0.0.0", port=5216)


    def find(self, idx, st):
        '''
        multifile find
        :param idx:
        :param st:
        :return:
        '''

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