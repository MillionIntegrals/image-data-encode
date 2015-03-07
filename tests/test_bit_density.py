__author__ = 'jrx'


import numpy as np

from numpy.testing import assert_array_equal
from nose.tools import assert_equal


from encoder.bit_density import convert_from_bit_density, convert_to_bit_density


def test_small_input():
    initial = np.array([0, 1, 255], dtype=np.uint8)
    converted = convert_to_bit_density(initial, 12)
    and_back = convert_from_bit_density(converted, 12)

    assert_array_equal(initial, and_back)


def test_random_input():
    for i in range(10):
        random_input = np.random.random_integers(0, 255, np.random.randint(10, 100)).astype(np.uint8)
        random_bit_density = np.random.randint(2, 20)

        converted = convert_to_bit_density(random_input, random_bit_density)
        and_back = convert_from_bit_density(converted, random_bit_density)

        assert_equal(converted.dtype, np.uint64)
        assert_equal(and_back.dtype, np.uint8)

        assert_array_equal(random_input, and_back[:len(random_input)])


def test_fixed_cases():
    initial = np.array([0, 1, 255], dtype=np.uint8)
    converted = convert_to_bit_density(initial, 12)
    assert_array_equal(converted, np.array([0, 511], dtype=np.uint64))


