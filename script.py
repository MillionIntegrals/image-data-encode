__author__ = 'jrx'

import PIL.Image as Image
import numpy as np

from bit_density import convert_from_bit_density, convert_to_bit_density, pad_bit_array, truncate_bit_array


# BLOCK_SIZE = 64
BLOCK_SIZE = 64 * 64

BITS_PER_BLOCK = int(np.log2(BLOCK_SIZE))
CHANNELS = (0, 1, 2)
BIT_DEPTH = 8

BLOCK_TEMPLATE = np.arange(BLOCK_SIZE, dtype=np.uint64)


def add_length_info(data):
    """ Add 64-bit length information at the beginning of data """
    length = len(data)
    length_arr = np.array([length], dtype=np.dtype('>u8')).view(np.uint8)
    return np.hstack((length_arr, data))


def strip_length_info(data):
    """ Strip 64-bit length information and truncate the data """
    length = data[:8].view(np.dtype('>u8'))[0]
    return data[8:8+length]


def read_data(bits, block_size):
    block_bits = bits.reshape((bits.shape[0] / block_size, block_size))
    return np.bitwise_xor.reduce(block_bits * BLOCK_TEMPLATE, axis=1)


def encode_data(input_bits, payload, block_size):
    block_bits = input_bits.reshape((input_bits.shape[0] / block_size, block_size))
    current_data = np.bitwise_xor.reduce(block_bits * BLOCK_TEMPLATE, axis=1)
    extra_length = current_data.shape[0] - payload.shape[0]
    payload = np.hstack((payload, current_data[-extra_length:]))
    diff = np.bitwise_xor(current_data, payload)
    block_bits[np.arange(block_bits.shape[0]), diff] = 1 - block_bits[np.arange(block_bits.shape[0]), diff]
    output_bits = block_bits.reshape(block_bits.shape[0] * block_bits.shape[1])
    return output_bits


def main():
    data = np.fromfile('data/DATA', dtype=np.uint8)
    data = add_length_info(data)
    bit_data = convert_to_bit_density(data, BITS_PER_BLOCK)  # DATA TO ENCODE

    im = Image.open('data/example.jpg')
    print("Image opened")
    assert im.mode == 'RGB', 'Only RGB mode images are supported!'

    print('Format', im.format, im.size, im.mode)

    # CONVERT IMAGE TO BITS
    rgb = np.array(im)
    shape = rgb.shape
    initial_img_length = shape[0] * shape[1] * shape[2]

    raw_data = rgb.reshape(initial_img_length)
    raw_bits = np.unpackbits(raw_data)
    raw_bits = pad_bit_array(raw_bits, BLOCK_SIZE)

    current_data = read_data(raw_bits, BLOCK_SIZE)

    encoded_bits = encode_data(raw_bits, bit_data, BLOCK_SIZE)

    encoded_data = np.packbits(truncate_bit_array(encoded_bits, 8))
    encoded_img_data = encoded_data[:initial_img_length].reshape(shape)

    Image.fromarray(encoded_img_data).save('output.jpg')

    pass


if __name__ == '__main__':
    main()
