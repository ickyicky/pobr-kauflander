# Kauflander

Recognizes Kaufland logo using simple image processing methods.

## Usage

Call it as module, for example: `python3 -m kauflander input.png output.png`.

Full usage is accessible via `--help` parameter:

```
usage: __main__.py [-h] [-s SIZE_FACTOR] [-g] [-m] [-e] [-f SEGMENT_MINIMUM_SIZE]
                   [-t SEGMENT_MAXIMUM_SIZE] [-r {mask,box}] [--show-color-mask]
                   [--show-segments] [--show-shapes]
                   FILE [FILE]

positional arguments:
  FILE                  input file
  FILE                  output file

options:
  -h, --help            show this help message and exit
  -s SIZE_FACTOR, --size-factor SIZE_FACTOR
                        size factor, multiplicator
  -g, --filter-gaussian
                        filter with gaussian filter
  -m, --filter-median   filter with median filter
  -e, --equallize-histogram
                        equallize histogram
  -f SEGMENT_MINIMUM_SIZE, --segment-minimum-size SEGMENT_MINIMUM_SIZE
                        minimum segment size in percentage in 1d
  -t SEGMENT_MAXIMUM_SIZE, --segment-maximum-size SEGMENT_MAXIMUM_SIZE
                        maximum segment size in percentage in 1d
  -r {mask,box}, --result {mask,box}
                        What result to produce, either mask or original image with
                        bounging box
  --show-color-mask     shows color mask
  --show-segments       shows all segments
  --show-shapes         shows all recognized shapes
```
