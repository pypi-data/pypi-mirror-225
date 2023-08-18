# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

import re
from os import path, access, R_OK
from numpy import argsort, flip
from .helper import format_header, round_sigfig, find_files, findall_infile
from . import cli


def findall_snips(regex: str, filepath: str, check_exist: bool = True) -> list:
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
    snips : list
        Results from re.findall function
    """
    regex_snips = (
        r"(?i)(\n|\r)(def|class|if __n|import|from)"
        + r"((\n|\r|.)*?)(?=(\ndef|\nclass|\rdef|\rclass|$))"
    )
    if (not path.exists(filepath)) and check_exist:
        return []
    if not access(filepath, R_OK):
        return []
    with open(filepath, "r", encoding="utf-8") as file:
        filetext = file.read()
    results = re.findall(regex, filetext)
    if len(results) == 0:
        return []
    snips = re.findall(regex_snips, filetext)
    return snips


def findall_pernewline(regex: str, text: str, filepath: str) -> dict:
    """Run re.findall function and find the number of newlines.
    Calculate a score as number of regex found divided by
    number of newlines found.

    Parameters
    ----------
    regex : str
        Regular expression
    text : str
        Text to search through
    filepath : str
        Full path to file text originated in

    Returns
    -------
    result : dict
        Regex search result each with keys:
        ["text","path","strings","string_num","newline_num","score"]

    """
    regex_newline = r"(\n|\r)+"
    strings_found = re.findall(regex, text)
    newlines_found = re.findall(regex_newline, text)
    if len(newlines_found) == 0:
        newlines_found = [""]
    result = {
        "text": text,
        "path": filepath,
        "strings": strings_found,
        "string_num": len(strings_found),
        "newline_num": len(newlines_found),
        "score": len(strings_found) / len(newlines_found),
    }
    return result


def search_all_pyfiles(searchpath: str, searchlist: list[str]) -> list[dict]:
    """Search for all strings in searchlist in every Python file
    found in the nested directories of searchpath. Each .py files is divided
    into code snippets before being searched (functions, classes). A similarity score
    is calculated by finding the number of strings found divided by the number
    of newlines in the code snippet.

    Parameters
    ----------
    searchpath : str
        Full path containing some .py files in nested folders
    searchlist : list[str]
        List of strings to search within files

    Returns
    -------
    ordered_search_results : list[dict]
        List of Regex search results each with keys:
        ["text","path","strings","string_num","newline_num","score"]
    """
    searchpath = path.abspath(searchpath)
    searchlist = [re.escape(searchterm) for searchterm in searchlist]
    regex_search = r"(?i)(" + "|".join(searchlist) + ")"
    _none, filelist = find_files(searchpath, ext=".py")
    snips_allfiles = [findall_snips(regex_search, pypath) for pypath in filelist]
    search_results = [
        findall_pernewline(regex_search, snip[2], filelist[i])
        for i, snips in enumerate(snips_allfiles)
        for snip in snips
    ]
    scores = [res["score"] for res in search_results]
    best_score_order = flip(argsort(scores))
    ordered_search_results = [
        search_results[i] for i in best_score_order if search_results[i]["score"] > 0
    ]
    return ordered_search_results


def get_result_str(ordered_search_results: list[dict], number: int = 5) -> str:
    """
    Parameters
    ----------
    ordered_search_results: list[dict]
        search result dictionaries ordered by score
    number: int
        Default = 5
        Number of results to add to output string
    Returns
    -------
    outstr : str
        All output results converted to string, concatenated, and output in a
        specific format.
    """
    outstr = ""
    for i, res in enumerate(ordered_search_results[0:number]):
        header = format_header(f"#{i+1} Result")
        outstr += f"\n{header}\n"
        outstr += f"    score: {round_sigfig(res['score'],4)} matches per newline\n"
        outstr += f"    match number: {res['string_num']}\n"
        outstr += f"    newline number: {res['newline_num']}\n"
        outstr += f"    path: {res['path']}\n"
        outstr += f"    code snip:\n\n{res['text']}\n\n"
    if len(outstr) == 0:
        outstr = "\nNo Results Found! Try different search keywords.\n"
    return outstr


def cli_main():
    """run main cli function"""
    args = cli.parse()
    searchdir, number, searchterms = [args[key] for key in args.keys()]
    results = search_all_pyfiles(searchdir, searchterms)
    resultstr = get_result_str(results, number=number)
    print(resultstr)
