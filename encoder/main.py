__author__ = 'jrx'

import argparse
import PIL.Image as Image
import numpy as np


from encoder.algorithms.xor_encoding import XorEncoding


def instantiate_algorithm(args):
    """ Instantiate algorithm object from given args """
    if args.algorithm == 'xor_encoding':
        return XorEncoding(block_size=args.block_size, intensity=args.intensity)

    raise RuntimeError('Algorithm type not detected')


def info_action(args):
    """ Run info action """
    if not args.infile:
        raise RuntimeError('You must specify infile for this action')

    algorithm = instantiate_algorithm(args)

    im = Image.open(args.infile)
    assert im.mode == 'RGB', 'Only RGB mode images are supported!'
    rgb_data = np.array(im)


    capacity = algorithm.data_capacity(rgb_data.shape)
    print(capacity)

    # print('Data capacity {:.2f} b/{:.2f} kb/{:.2f} mb'.format(capacity, capacity / 1024, capacity / 1024 / 1024))


def encode_action(args):
    """ Run encode action """
    if not args.infile:
        raise RuntimeError('You must specify infile for this action')

    if not args.outfile:
        raise RuntimeError('You must specify outfile for this action')

    if not args.datafile:
        raise RuntimeError('You must specify datafile for this action')

    algorithm = instantiate_algorithm(args)

    im = Image.open(args.infile)
    assert im.mode == 'RGB', 'Only RGB mode images are supported!'

    data_payload = np.fromfile(args.datafile, dtype=np.uint8)

    input_rgb_data = np.array(im)
    output_rgb_data = algorithm.encode(input_rgb_data, data_payload)

    output_img = Image.fromarray(output_rgb_data, 'RGB')
    output_img.save(args.outfile)


def decode_action(args):
    """ Run decode action """
    if not args.infile:
        raise RuntimeError('You must specify infile for this action')

    if not args.outfile:
        raise RuntimeError('You must specify outfile for this action')

    algorithm = instantiate_algorithm(args)

    im = Image.open(args.infile)
    assert im.mode == 'RGB', 'Only RGB mode images are supported!'

    input_rgb_data = np.array(im)
    output_payload = algorithm.decode(input_rgb_data)
    output_payload.tofile(args.outfile)


def main():
    parser = argparse.ArgumentParser(description='Encode data in your images')
    parser.add_argument('action', choices=['info', 'encode', 'decode'],
                        help="Specify which action you want to choose")

    parser.add_argument('-i', '--infile', help='Specify input file', default='')
    parser.add_argument('-o', '--outfile', help='Specify output file', default='')
    parser.add_argument('-a', '--algorithm', help='Choose your algorithm', default='xor_encoding')
    parser.add_argument('-d', '--datafile', help='Specify data file', default='')

    group = parser.add_argument_group('Algorithm parameters')

    group.add_argument('--block_size', type=int, help='Algorithm block size', default=64*64)
    group.add_argument('--intensity', type=int, choices=[x + 1 for x in range(8)],
                       help='Algorithm intensity', default=8)

    args = parser.parse_args()

    if args.action == 'info':
        info_action(args)

    if args.action == 'encode':
        encode_action(args)

    if args.action == 'decode':
        decode_action(args)


if __name__ == '__main__':
    main()