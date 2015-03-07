__author__ = 'jrx'

import numpy as np

from encoder.constants import BITS_PER_BYTE


def truncate_bit_array(bit_array, bit_length):
    """ Truncate given bit-array (uint8), so that the length can be divided by bit_length without a remainder """
    overflow = bit_array.shape[0] % bit_length

    if overflow > 0:
        return bit_array[:-overflow]
    else:
        return bit_array


def pad_bit_array(bit_array, bit_length):
    """ Pad given bit-array (uint8) with zeros, so that the length can be divided by bit_length without a remainder """
    missing_bits = (bit_length - (bit_array.shape[0] % bit_length)) % bit_length

    # PAD BITS IF NEEDED
    if missing_bits > 0:
        missing = np.repeat(0, missing_bits).astype(np.uint8)
        return np.hstack((bit_array, missing))
    else:
        return bit_array


def convert_to_bit_density(input_data, result_density):
    """ Convert array bit density from uint8 to specified density uint64 """
    assert len(input_data.shape) == 1, 'This method works only on 1-D data'

    bits = np.unpackbits(input_data)
    bits = pad_bit_array(bits, result_density)

    assert bits.shape[0] % result_density == 0, 'Make sure that length is ok'

    reshaped = bits.reshape((bits.shape[0] // result_density, result_density))
    mask = (2 ** np.arange(result_density, dtype=np.uint64)[::-1]).reshape((1, result_density))
    return np.sum(reshaped * mask, axis=1)


def convert_from_bit_density(input_data, result_density):
    """ Convert from given density (uint64) to uint8 """
    input_shape = input_data.shape[0]
    raw_bits = np.unpackbits(input_data.astype(np.dtype('>u8')).view(np.uint8)).reshape(input_shape, 64)
    truncated_bits = raw_bits[:, -result_density:]
    truncated_bits = truncated_bits.reshape(truncated_bits.shape[0] * truncated_bits.shape[1])

    truncated_bits = pad_bit_array(truncated_bits, BITS_PER_BYTE)

    return np.packbits(truncated_bits)
