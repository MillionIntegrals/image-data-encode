# img-data-encode

My small hobby python project to test an algorithm idea I've had once about how one can encode arbitrary data in an image without changing it visually too much.

Sadly, it only works when you save images in a lossless compression format such as PNG. 

### Usage

Program is invoked by calling the encoder/main.py file. Here is the brief help information:

```
mi@mihome ~/repos/img-data-encode> python3 -m encoder.main -h
usage: main.py [-h] [-i INFILE] [-o OUTFILE] [-a ALGORITHM] [-d DATAFILE]
               [--block_size BLOCK_SIZE] [--intensity {1,2,3,4,5,6,7,8}]
               {info,encode,decode}

Encode data in your images

positional arguments:
  {info,encode,decode}  Specify which action you want to choose

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        Specify input file
  -o OUTFILE, --outfile OUTFILE
                        Specify output file
  -a ALGORITHM, --algorithm ALGORITHM
                        Choose your algorithm
  -d DATAFILE, --datafile DATAFILE
                        Specify data file

Algorithm parameters:
  --block_size BLOCK_SIZE
                        Algorithm block size
  --intensity {1,2,3,4,5,6,7,8}
                        Algorithm intensity
```

You invoke action *info* to see how much bytes of data you can write to given image with supplied algorithm settings.
Henerally, the higher the intensity and lower the block size the more data you can write to given image. But if you specify intensity too high or block size too low distortions may become visible in the image.

This action only needs an *infile* and algorithm parameters.

To invoke action *encode* you need all *infile*, *outfile* and a *datafile* (plus the algorithm options). If given algorithm options give you enough data capacity to save all the data you wanted, everything should go smoothly.

To decode, specify action *decode*, an *infile* to be the previously encoded image, and an *outfile* as where to save the data to. Algorithm options must be the same as in the encoding step. Decoded data will be saved to the outfile path.

Block size specified must be a power of two.


### How does it work

When I have some time, I'll write an explaination how the algorithm works. Feel free to contact me if you'd be interested in seeing it.

# Example

Here is the image of a dragon I've downloaded from Flickr:

![dragon](https://raw.githubusercontent.com/MillionIntegrals/img-data-encode/master/data/dragon.jpg)

And this is the same image with the whole Alice in Wonderland (160kb) text encoded in it. Parameters were block_size=8, intensity=4.

![dragon encoded](https://raw.githubusercontent.com/MillionIntegrals/img-data-encode/master/data/dragon_encoded.png)
