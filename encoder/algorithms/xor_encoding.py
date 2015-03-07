__author__ = 'jrx'

import numpy as np

from encoder.bit_density import pad_bit_array, convert_to_bit_density, convert_from_bit_density
from encoder.constants import BITS_PER_BYTE, BYTES_PER_UINT64
from encoder.utilities import add_length_info, strip_length_info


class XorEncoding:

    def __init__(self, block_size, intensity):
        self.bits_per_block = block_size
        self.block_size = 2 ** self.bits_per_block
        self.intensity = intensity
        self.block_template = np.arange(self.block_size, dtype=np.uint64)

    def data_capacity(self, img_size):
        """ Return data capacity for given algorithm and image -- in bytes """
        bits_in_image = img_size[0] * img_size[1] * img_size[2] * self.intensity
        number_of_blocks = bits_in_image // self.block_size
        return number_of_blocks * self.bits_per_block // BITS_PER_BYTE - BYTES_PER_UINT64
    
    def _pack_data(self, data):
        """ 
        :param data: 1-D uint8 raw data to encode
        :return: 1-D uint64 data encoded
        """
        length_data = add_length_info(data)
        return convert_to_bit_density(length_data, self.bits_per_block)  # DATA TO ENCODE

    def _unpack_data(self, packed_data):
        """
        :param data: 1-D uint64 data to return
        :return: 1-D uint8 array decoded
        """
        payload_8bit = convert_from_bit_density(packed_data, self.bits_per_block)
        return strip_length_info(payload_8bit)

    def _encoding_algorithm(self, image_bits, packed_data):
        """
        Encode data in image bit data

        :param image_bits: flat 1-D uint8 bit array of bits in the image
        :param packed_data: flat 1-D uint64 array of packed data to encode
        :return: encoded 1-D uint8 bit array of bits in the image
        """
        padded_image_bits = pad_bit_array(image_bits, self.block_size)
        block_bits = padded_image_bits.reshape((padded_image_bits.shape[0] // self.block_size, self.block_size))
        current_data = np.bitwise_xor.reduce(block_bits * self.block_template, axis=1)

        original_payload_length = packed_data.shape[0]

        assert len(current_data) >= len(packed_data), "Image does not have enough capacity to save this data"

        # Bits to change
        diff = np.bitwise_xor(current_data[:original_payload_length], packed_data)

        block_bits[np.arange(original_payload_length), diff] = 1 - block_bits[np.arange(original_payload_length), diff]
        return block_bits.flatten()[:image_bits.shape[0]]

    def _decoding_algorithm(self, image_bits):
        """
        Decoda data from image bit data

        :param image_bits: A 1-d uint8 bit array of the image
        :return: decoded packed 1-D uint64 data from the image
        """
        padded_image_bits = pad_bit_array(image_bits, self.block_size)
        block_bits = padded_image_bits.reshape((padded_image_bits.shape[0] // self.block_size, self.block_size))
        return np.bitwise_xor.reduce(block_bits * self.block_template, axis=1)

    def encode(self, img_data, payload):
        """
        Encode image data
        :param img_data: w x h x 3 uint8 numpy array of image colors
        :param payload: 1-D uint8 raw payload data to encode
        :return: encoded w x h x 3 uint8 numpy array of image colors
        """
        """ Encode image data """
        packed_payload = self._pack_data(payload)

        # Prepare image data
        shape = img_data.shape
        initial_img_length = shape[0] * shape[1] * shape[2]

        raw_data = img_data.flatten()
        raw_bits = np.unpackbits(raw_data).reshape(initial_img_length, BITS_PER_BYTE)

        selected_raw_bits = raw_bits[:, -self.intensity:].flatten()

        # Actual encoding part
        output_bits = self._encoding_algorithm(selected_raw_bits, packed_payload)
        output_bits = output_bits.reshape(initial_img_length, self.intensity)
        raw_bits[:, -self.intensity:] = output_bits

        # Pack the result again
        return np.packbits(raw_bits).reshape(shape)

    def decode(self, img_data):
        """
        Decode image data
        :param img_data: w x h x 3 unit8 numpy array of image colors
        :return: 1-d uint8 data encoded in the image
        """
        # Prepare image data
        shape = img_data.shape
        initial_img_length = shape[0] * shape[1] * shape[2]

        raw_data = img_data.flatten()
        raw_bits = np.unpackbits(raw_data).reshape(initial_img_length, BITS_PER_BYTE)

        selected_raw_bits = raw_bits[:, -self.intensity:].flatten()

        packed_payload = self._decoding_algorithm(selected_raw_bits)
        return self._unpack_data(packed_payload)
