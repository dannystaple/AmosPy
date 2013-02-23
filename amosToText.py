"""Main script of this package - this will convert
an amos tokenised file into plain text, which should be
a representation of what you'd have seen in the Amos editor
window."""
from __future__ import print_function
import sys
from AmosPy.converter import Converter


def output_file(filename):
    converter = Converter()
    items = converter.do_file(filename)
    header = next(items)
    try:
        [print(line) for line in items]
    finally:
        print("Code Bytes read", converter.bytes_read, "of", header['length'])
        if converter.unknown_tokens:
            print("Found %d unknown tokens" % converter.unknown_tokens)
    if converter.unknown_tokens == 0 and converter.bytes_read == header['length']:
        print("All tokens translated")


if __name__ == '__main__':
    output_file(sys.argv[1])
