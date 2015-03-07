__author__ = 'jrx'


import numpy as np

from numpy.testing import assert_array_equal
from nose.tools import assert_greater, assert_equal


from encoder.algorithms.xor_encoding import XorEncoding


def test_capacity_monotonic():
    shape = (640, 480, 3)

    base = XorEncoding(block_size=6, intensity=4)
    low_block = XorEncoding(block_size=5, intensity=4)
    high_intensity = XorEncoding(block_size=5, intensity=8)

    assert_greater(low_block.data_capacity(shape), base.data_capacity(shape))
    assert_greater(high_intensity.data_capacity(shape), base.data_capacity(shape))

    assert_equal(base.data_capacity(shape), 43192)
    assert_equal(low_block.data_capacity(shape), 71992)
    assert_equal(high_intensity.data_capacity(shape), 143992)


def test_base():
    image = np.random.randint(0, 256, (640, 480, 3)).astype(np.uint8)
    encoding = XorEncoding(block_size=6, intensity=4)
    max_size = encoding.data_capacity(image.shape)

    data = np.random.randint(0, 256, max_size).astype(np.uint8)

    encoded = encoding.encode(image, data)

    assert_equal(encoded.dtype, np.uint8)
    assert_equal(encoded.shape, image.shape)

    decoded = encoding.decode(encoded)

    assert_equal(decoded.dtype, np.uint8)
    assert_equal(decoded.shape, data.shape)

    assert_array_equal(data, decoded)


def test_high_intensity():
    image = np.random.randint(0, 256, (640, 480, 3)).astype(np.uint8)
    encoding = XorEncoding(block_size=6, intensity=8)
    max_size = encoding.data_capacity(image.shape)

    data = np.random.randint(0, 256, max_size).astype(np.uint8)

    encoded = encoding.encode(image, data)

    assert_equal(encoded.dtype, np.uint8)
    assert_equal(encoded.shape, image.shape)

    decoded = encoding.decode(encoded)

    assert_equal(decoded.dtype, np.uint8)
    assert_equal(decoded.shape, data.shape)

    assert_array_equal(data, decoded)


def test_low_block():
    image = np.random.randint(0, 256, (640, 480, 3)).astype(np.uint8)
    encoding = XorEncoding(block_size=1, intensity=1)
    max_size = encoding.data_capacity(image.shape)

    data = np.random.randint(0, 256, max_size).astype(np.uint8)

    encoded = encoding.encode(image, data)

    assert_equal(encoded.dtype, np.uint8)
    assert_equal(encoded.shape, image.shape)

    decoded = encoding.decode(encoded)

    assert_equal(decoded.dtype, np.uint8)
    assert_equal(decoded.shape, data.shape)

    assert_array_equal(data, decoded)


