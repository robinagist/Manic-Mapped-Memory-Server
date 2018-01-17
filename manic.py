import mmap, time

'''
Manic - hella fast memory mapped data tables

'''




def m_open(filename):
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


def m_index(mm):
    '''
    creates the indices for the memory mapped score file
    :param mm: memory mapped file reference
    :returns: dicts: hand to position, hashed hand to position, hashed hand score to position

    the line to index looks like this - it's 94 characters long
    0--------+---------+---------+---------+---------+---------+---------+---------+---------+----
    2C 2D 2H 2S 3D,000000005003,2c44e44bf3c26515b9142870a69d308b,cdb2bf151bafd21a2591f1690a4c7339\n

    '''
    # because you weren't kind, i have to rewind
    pos = 0
    chunk_size = 94
    h_d = dict()
    hh_d = dict()
    hhs_d = dict()

    # go through the file line by line, making an index
    while(True):
        mm.seek(pos)
        line = bytes.decode(mm.readline())
        if len(line) < 94:
            break
        h, s, hh, hhs = line.strip().split(',')
 #       print(h, s, hh, hhs, pos)
        h_d[h] = pos
        hh_d[hh] = pos
        hhs_d[hhs] = pos
        pos += chunk_size

    return h_d, hh_d, hhs_d


def find(mm, index, target):
    '''
    given a hand, hashed_handed or a hashed hand score, return a dict with the matchine entry
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