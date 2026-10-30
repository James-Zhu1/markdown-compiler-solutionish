#!/usr/bin/python3

"""
Command line interface for the markdown compiler.
"""
from markdown_compiler import *


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', required=True)
    parser.add_argument('--add_css', action='store_true')
    args = parser.parse_args()
    convert_file(args.input_file, args.add_css)


if __name__ == '__main__':
    main()
