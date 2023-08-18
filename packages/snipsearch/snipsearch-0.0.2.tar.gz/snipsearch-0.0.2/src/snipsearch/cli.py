# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""
from argparse import ArgumentParser, REMAINDER


def parse():
    """Run command line parsing"""
    desc = "Find code snippets which are most related to search keywords."
    dirh = "Directory containing Python (.py) files to search through"
    keywordh = (
        "List as many strings as you would like to search for (all equally weighted)"
    )
    numh = "Number of code snippet results to print"
    parser = ArgumentParser(prog="snipsearch", description=desc)
    parser.add_argument("searchdir", help=dirh)
    parser.add_argument("-n", "-number", default=5, type=int, help=numh)
    parser.add_argument("searchterms", nargs=REMAINDER, help=keywordh)
    args = vars(parser.parse_args())
    print(f"\nCommand Line Args:\n{args}\n")
    return [args[key] for key in args.keys()]
