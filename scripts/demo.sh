#!/bin/bash

if ! [ -d output ]; then
    mkdir output
fi

echo "Encoding marocco..."
python3 -m encoder.main encode -i data/marocco.jpg -o output/marocco_encoded.png -d data/ALICE_IN_WONDERLAND --intensity=2 --block_size=6
echo "Decoding marocco..."
python3 -m encoder.main decode -i output/marocco_encoded.png -o output/marocco_decoded.txt --intensity=2 --block_size=6

echo "Encoding dragon..."
python3 -m encoder.main encode -i data/dragon.jpg -o output/dragon_encoded.png -d data/ALICE_IN_WONDERLAND --intensity=4 --block_size=3
echo "Decoding dragon..."
python3 -m encoder.main decode -i output/dragon_encoded.png -o output/dragon_decoded.txt --intensity=4 --block_size=3

echo "Done"
