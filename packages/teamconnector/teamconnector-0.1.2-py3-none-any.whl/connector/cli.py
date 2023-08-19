#!/usr/bin/env python3
"""
connector-cli (18 August 2023)
This is a basic Python Script template

example:
    $ python3 argparse-template.py "hello" 123 --enable

(C) 2023, TJ Singh lab (singhlab@nygenome.org)
Source: www.github.com/tjsinghlab/
License: GNU General Public License v3
"""

__author__ = "Tarjinder Singh"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import sys
import subprocess
import argparse
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_arguments():
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("arg", help="Required positional argument")
    parser.add_argument("-f", "--flag", action="store_true", default=False)
    parser.add_argument("-c", "--count", default=5, type=int)
    parser.add_argument("-n", "--name", action="store", dest="name")
    #parser.add_argument(
    #    '-f', "--file", type=argparse.FileType('r'), help="file to be copied")
    parser.add_argument(
        "-s", "--select", choices=['rock', 'paper', 'scissors'], default="rock")
    parser.add_argument("-v", "--verbose", action="count",
                        default=0, help="Verbosity (-v, -vv, etc)")
    parser.add_argument("--version", action="version",
                        version="%(prog)s (version {version})".format(version=__version__))
    return(parser.parse_args())


def main():
    """ Main entry point of the app """
    args = parse_arguments()
    args = args.__dict__
    logger.info("hello world")
    logger.info(args)
    for line in args.f:
        print(line.strip())


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
