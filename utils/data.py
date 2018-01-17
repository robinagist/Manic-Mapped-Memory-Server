import mmap

'''
utility methods for data processing
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
    d["names"] = colnames

    # set up skip and chomp defaults
    d["skip"] = 0
    d["chomp"] = 0

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

def create(filename):
    '''
    loads the score file into a memory mapped file, then write protects it
    :param filename: the score file to load into a memory map
    :return:
    '''

    lock = mmap.ACCESS_READ

    with open(filename, "r") as readfile:
        mm = mmap.mmap(readfile.fileno(),length=0, access=lock)
        # be kind and rewind
        mm.seek(0)
        readfile.close()
        return mm


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
        delim = cis["delim"]
        read_ahead_lines = cis["chomp"]
        llnl = cis["llnl"]
        idx_names = cis["names"]

        # create the index structures

        for idx in idx_names:
            if not idx:
                _idx.append(None)
            _idx.append(dict())

        # go through the file line by line, making an index
        while(True):
            line_l = 0
            print(pos)
            mm.seek(pos)
            try:
                line = bytes.decode(mm.readline())
            except:
                break

            ## checks
            # line by itself is end of file
            if llnl and line == '\n':
                break
            if line == None:
                break
            # read ahead at beginning of file
            # TODO - do not use yet
            if read_ahead_lines:
                read_ahead_lines-=1
                continue


            # now index
            line_l = len(line)
            vals = line.strip().split(delim)

            cc = -1
            for idx in _idx:
                cc += 1
                if not idx:
                    continue
                v = vals[cc]
                idx[v] = pos

            # forward to next line
            pos += line_l

        dd = dict()
        cc = -1
        for idx in idx_names:
            cc += 1
            if not idx:
                continue
            dd[idx] = _idx[cc]

    return dd


def find(mm, index, target):
    '''
    return a line with the matching entry
    :param target: a string containing the lookup criteria (hand, hashed hand, hashed hand score)
    :param index: dict - the index to use to search
    :return: a dict containing the hand, padded score, hashed handed, and hashed hand score
    '''

    pos = 0
    mm.seek(pos)

    try:
        pos = index[target]
        if not pos:
            return None
        mm.seek(pos)
    except:
        return None

    return bytes.decode(mm.readline())



def m_rewind(mm):
    return mm.seek(0)


def m_close(mm):
    '''
    close the memory mapped file passed in
    :param mm:
    :return:
    '''
    return mm.close()