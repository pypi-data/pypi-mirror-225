import argparse
import os
from io import StringIO


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-i", "--input", help="Input .bin file", required=True)
arg_parser.add_argument("-o", "--output", help="Output .hex file", required=False)

args = arg_parser.parse_args()

input_file = args.input
output_file = args.output

if not (os.path.exists(input_file) and os.path.isfile(input_file)):
    print("Cannot read {}.".format(input_file))
    exit(1)

if not output_file:
    output_file = input_file + ".hex"

with open(input_file, "rb") as ifile:
    hex = ifile.read().hex()
    hex_len = int(len(hex) / 2)
    print("File length: {:,} bytes.".format(hex_len).replace(',', '`'))
    output_hex = StringIO()
    with open(output_file, "w") as ofile:
        for i in range(hex_len):
            hex_byte = hex[i * 2:i * 2 + 2]
            output_hex.write(hex_byte + " ")
            if (i + 1) % 20 == 0:
                output_hex.write("\n")
        if hex_len < 400:
            print(output_hex.getvalue())
        ofile.write(output_hex.getvalue())
