import time

'''
general utilities for manic
'''

def start_clock():
    '''
    timer for high precision measuring in microseconds
    :return: current clock time
    '''
    return time.clock()

def end_clock(start_time):
    '''
    returns the delta from start time in milliseconds
    :param start_time:
    :return:
    '''
    #microsecond resolution
    exec_time = (time.clock() - start_time)
    # millisecond resolution
    exec_time *= 1000
    return "{:5.6f}".format(exec_time)


def clock(func):
    '''
    decorator for the clock
    :param func:
    :return:
    '''
    def wrapper(find_func):
        start_time = start_clock()
        find_func()
        return end_clock(start_time)