import mmap, time, os
from utils.utils import start_clock, end_clock
import config, json

'''
utility methods for index and memory map processing
'''


def define_columns_using_delimiter(colnames, delim=','):
    '''

    defines the columns of the data file as separated by a delimiter

    :param colnames: list - an ordered list of column names
    :param delim: string - the
    :return: a data structure to be used by the indexing method

    note:  if a column of data is not to be indexed (e.g. no lookups will be performed)
    in place of a field name, use _
    '''

    d = dict()
    d["type"] = "delim"
    d["delim"] = delim
    d["indexes"] = colnames

    # set up skip and chomp defaults
    d["skip"] = 0
    d["chomp"] = 0
    d["llnl"] = False

    return d


def define_column_actions(column_defs, delim=','):
    '''

    defines the columns of the data file as separated by a delimiter

    :param colnames: list - an ordered list of column names
    :param delim: string - the
    :return: a data structure to be used by the indexing method

    note:  if a column of data is not to be indexed (e.g. no lookups will be performed)
    in place of a field name, use _
    '''

    d = dict()
    d["type"] = "delim"
    d["delim"] = delim
    d["indexes"] = column_defs

    # set up skip and chomp defaults
    d["skip"] = 0
    d["chomp"] = 0
    d["llnl"] = False

    return d


def define_skip_startlines(n, cis):
    '''
    tells the parser to skip the first n lines before starting to read data
    :param n:
    :param cis:
    :return:
    '''
    cis["skip"] = n


def define_chomp_lastlines(n, cis):
    '''
    tells the parser to not include the last n lines of the file
    :param n:
    :param cis:
    :return:
    '''
    cis["chomp"] = n


def define_lastline_newline(cis, n=True):
    '''
    tells the parser to not include the last n lines of the file
    :param n:
    :param cis:
    :return:
    '''
    cis["llnl"] = n


def load_memfile_configs():
    '''
    creates a lookup for memfile names to configurations
    :return:
    '''

    # get the base directory
    basedir = config.BASE_PATH
    memfilesdir = config.MEMFILES_DIR
    fullpath = "{}/{}".format(basedir, memfilesdir)
    configs = list()

    for name in next(os.walk(fullpath))[1]:
        cfg = "{}/{}/{}".format(fullpath, name, "config.json")
        try:
            with open(cfg) as configfile:
                cis = json.load(configfile)
                cis["mmname"] = name
                configs.append(cis)
        except:
            raise Exception("missing config.json for {} ".format(name))

    return configs


def create(filename):
    '''
    loads the score file into a memory mapped file, then write protects it
    :param filename: the score file to load into a memory map
    :return:
    '''

    lock = mmap.ACCESS_READ

    with open(filename, "r") as readfile:
        mm = mmap.mmap(readfile.fileno(), length=0, access=lock)
        # be kind and rewind
        mm.seek(0)
        readfile.close()
        return mm


def mf_index(mmm_, cfgs_dict):
    '''
    index multiple memmap files
    :param mmm: dict() containing {"index_name":"<index_name>", "mapped_file":{<mapped_file>]
    :param cfg: dict() contains the configurations for each of the memfiles
    :return:
    '''

    cidx = {}
    # for each mapped file
    for cfg in cfgs_dict:
        # .. index the columns
        idxs = index(mmm_, cfg)
        # .. create index to index name
        for idx in idxs.keys():
            cidx[idx] = cf

    # .. map column index to mapped file (lookup)

    pass



def index(mm, cis):
    '''
    creates the indices for the memory mapped score file
    :param mm: memory mapped file reference
           cis: column indexing structure (created by a 'define_columns_xxx' method)
    :returns: dictionary of named dicts that contain the indices
    '''

    pos = 0
    _idx = list()

    if cis["type"] == "delim":
        # set up a read-ahead buffer
        delim = ","
        read_ahead_lines = cis["chomp"]
        llnl = cis["llnl"]

        # create the index structures
        idx_profiles = cis["indexes"]
        idx_names = [x["name"] for x in idx_profiles]
        idx_constraints = [x["constraint"] for x in idx_profiles]

        for _ in idx_names:
            _idx.append(dict())

        # go through the file line by line, making an index
        while(True):

            mm.seek(pos)
            try:
                line = bytes.decode(mm.readline())
            except:
                break

            ## checks
            # line by itself is end of file
            if llnl and line == '\n':
                break
            if len(line.strip()) == 0:
                break

            '''
            # read ahead at beginning of file
            # TODO - do not use yet
            if read_ahead_lines:
                read_ahead_lines-=1
                continue
            '''

            line_l = len(line)
            vals = line.strip().split(delim)
            cc = 0
            for idx in _idx:
                v = vals[cc]
                v = v.strip('\r\n')
                if idx_constraints[cc] == "NOINDEX":
                    cc += 1
                    continue
                # build the index
                if v in idx:
                    p = idx[v]

                    # already chained
                    if isinstance(p, set):
                        p.add(pos)

                    # one element exists -- add chain to add this element
                    elif isinstance(p, int):
                        if idx_constraints[cc] == "UNIQUE":
                            raise Exception("duplicate key `{}` found in column marked UNIQUE".format(v))
                        s = set()
                        s.add(p)
                        s.add(pos)
                        idx[v] = s
                else:

                    # no chain
                    idx[v] = pos
                cc += 1

            # forward to next line
            pos += line_l

        dd = dict()
        cc = 0
        for idx in idx_names:
            dd[idx] = _idx[cc]
            cc += 1

        return dd


def _find(mm, index, target):
    '''
    return a line with the matching entry
    :param target: a string containing the lookup criteria (hand, hashed hand, hashed hand score)
    :param index: dict - the index to use to search
    :return: a dict containing the entire result
             a floating point of the lookup time in milliseconds
    '''

    pos = 0
    mm.seek(pos)

    # empty index means no index on this column
    if len(index)==0:
        return 0, 0
    resp = set()
    try:
        s = start_clock()                # start lookup timer
        pos = index[target]
        # no result
        if not pos:
            return None, None
        if isinstance(pos, set):
            for p in pos:
                mm.seek(p)
                resp.add(bytes.decode(mm.readline()))
        else:
            mm.seek(pos)
            resp.add(bytes.decode(mm.readline()))

        e = end_clock(s)                 # end lookup timer
    except:
        return None, None

    return resp, e


def rewind(mm):
    return mm.seek(0)


def m_close(mm):
    '''
    close the memory mapped file passed in
    :param mm:
    :return:
    '''
    return mm.close()