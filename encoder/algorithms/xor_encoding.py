__author__ = 'jrx'

import numpy as np

from encoder.bit_density import pad_bit_array, truncate_bit_array, convert_to_bit_density, convert_from_bit_density
from encoder.utilities import add_length_info, strip_length_info


class XorEncoding:
    def __init__(self, block_size):
        self.block_size = block_size
        self.bits_per_block = int(np.log2(self.block_size))
        self.block_template = np.arange(self.block_size, dtype=np.uint64)

    def data_capacity(self, img_size):
        """ Return data capacity for given algorithm and image """
        bits_in_image = img_size[0] * img_size[1] * img_size[2] * 8
        number_of_blocks = bits_in_image // self.block_size
        return number_of_blocks * self.bits_per_block // 8 - 8

    def encode(self, img_data, payload):
        """ Encode image data """
        # PREPARE PAYLOAD
        length_payload = add_length_info(payload)
        bit_payload = convert_to_bit_density(length_payload, self.bits_per_block)  # DATA TO ENCODE

        # Prepare image data
        shape = img_data.shape
        initial_img_length = shape[0] * shape[1] * shape[2]

        raw_data = img_data.reshape(initial_img_length)
        raw_bits = np.unpackbits(raw_data)
        raw_bits = pad_bit_array(raw_bits, self.block_size)

        # Actual encoding part
        block_bits = raw_bits.reshape((raw_bits.shape[0] // self.block_size, self.block_size))
        current_data = np.bitwise_xor.reduce(block_bits * self.block_template, axis=1)
        original_payload_length = bit_payload.shape[0]
        # extra_length = current_data.shape[0] - bit_payload.shape[0]
        # bit_payload = np.hstack((bit_payload, current_data[-extra_length:]))
        diff = np.bitwise_xor(current_data[:original_payload_length], bit_payload)
        block_bits[np.arange(original_payload_length), diff] = 1 - block_bits[np.arange(original_payload_length), diff]
        output_bits = block_bits.reshape(block_bits.shape[0] * block_bits.shape[1])

        # Pack the result again
        encoded_data = np.packbits(truncate_bit_array(output_bits, 8))
        encoded_img_data = encoded_data[:initial_img_length].reshape(shape)

        return encoded_img_data

    def decode(self, img_data):
        """ Decode image data """
        # Prepare image data
        shape = img_data.shape
        initial_img_length = shape[0] * shape[1] * shape[2]

        raw_data = img_data.reshape(initial_img_length)
        raw_bits = np.unpackbits(raw_data)
        raw_bits = pad_bit_array(raw_bits, self.block_size)

        # Actual decoding
        block_bits = raw_bits.reshape((raw_bits.shape[0] // self.block_size, self.block_size))
        raw_payload = np.bitwise_xor.reduce(block_bits * self.block_template, axis=1)

        # Packing data back
        payload_8bit = convert_from_bit_density(raw_payload, self.bits_per_block)
        payload = strip_length_info(payload_8bit)
        return payload

