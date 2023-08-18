# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

import re
from os import walk, path
from math import log10, floor, ceil
from typing import Union, Tuple


def format_header(name: str, repeat_char: str = "-", linelen: int = 68) -> str:
    """Format a string header for printing or logging.

    Parameters
    ----------
    name : str
        String to include in middle of header
    repeat_char : str
        Character to repeat before and after name
    linelen : int
        Total length of string to create

    Returns
    -------
    header : str
        Full line string with name between repeated characters

    """
    start = repeat_char * floor((linelen - len(name) - 2) / 2)
    end = repeat_char * ceil((linelen - len(name) - 2) / 2)
    header = f"{start} {name} {end}"
    return header


def round_sigfig(number: Union[float, int], sigfig: int) -> Union[float, int]:
    """Round a number to a certain number of significant figures.

    Parameters
    ----------
    number : Union[float, int]
        Arbitrary number to round
    sigfig : int
        Number of significant digits

    Returns
    -------
    Union[float, int]

    """
    if number == 0:
        return 0
    return round(number, sigfig - int(floor(log10(abs(number)))) - 1)


def find_files(
    searchpath: str, ext: str = ".py", skip_hidden: bool = True
) -> Tuple[list[str], list[str]]:
    # CHANGE SKIP_HIDDEN TO BE A LIST OF SKIPABLE STARTS

    """Find all files in searchpath with a certain extension.

    Parameters
    ----------
    searchpath : str
        Full path to search all nested directories for files
    ext : str
        Extension of files to find

    Returns
    -------
    pathlist : list[str]
        Directories where files were found
    filelist : list[str]]
        All files found with given extension
    """
    pathlist = []
    filelist = []
    for root, dirs, files in walk(searchpath):
        if skip_hidden:
            dirs[:] = [
                dirname
                for dirname in dirs
                if not (dirname.startswith(".") or dirname.startswith("_"))
            ]
        contains_py = False
        for filename in files:
            _none2, fileext = path.splitext(filename)
            if ext == fileext:
                contains_py = True
                filepath = path.join(root, filename)
                filepath = filepath.replace("\\", "/")
                filelist.append(filepath)
        if contains_py:
            pathlist.append(root)
    return pathlist, filelist


def findall_infile(regex: str, filepath: str, check_exist: bool = True) -> list:
    """Open ascii file for reading and get results of re.findall

    Parameters
    ----------
    regex : str
        Regular expression
    filepath : str
        Path of ascii text file to search
    check_exist : bool
        True to return empty list if file does not exist

    Returns
    -------
    results : list
        Results from re.findall function
    """
    if (not path.exists(filepath)) and check_exist:
        return []
    with open(filepath, "r", encoding="utf-8") as file:
        filetext = file.read()
    results = re.findall(regex, filetext)
    return results
