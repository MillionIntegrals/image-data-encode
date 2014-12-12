__author__ = 'jrx'

import numpy as np


def add_length_info(data):
    """ Add 64-bit length information at the beginning of data """
    length = len(data)
    length_arr = np.array([length], dtype=np.dtype('>u8')).view(np.uint8)
    return np.hstack((length_arr, data))


def strip_length_info(data):
    """ Strip 64-bit length information and truncate the data """
    length = data[:8].view(np.dtype('>u8'))[0]
    return data[8:8+length]