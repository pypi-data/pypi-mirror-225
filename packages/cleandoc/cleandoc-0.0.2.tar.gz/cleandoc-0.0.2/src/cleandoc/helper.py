# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from subprocess import run
from math import floor, ceil
from typing import Tuple
from os import path, walk, remove
from datetime import datetime
from re import findall
import logging
from sys import stdout


def run_capture_out(cmd: list[str], shell: bool = False) -> Tuple[str, str]:
    """Run subprocess command and return the stdout and stderr.

    Parameters
    ----------
    cmd : list[str]
        Pass list of shell commands to subprocess.run
    shell : bool
        Pass shell keyword argument to subprocess.run

    Returns
    -------
    stdout  : str
        Standard Output returned from shell
    stderr : str
        Standard Error returned from shell

    """
    proc = run(
        cmd,
        capture_output=True,
        encoding="utf-8",
        check=False,
        shell=shell,
        errors="ignore",
    )
    return proc.stdout, proc.stderr


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


def find_pyfiles(searchpath: str) -> Tuple[list[str], list[str]]:
    """Find all .py files in nested directories.

    Parameters
    ----------
    searchpath : str
        Full path to search through for .py files

    Returns
    -------
    pathlist : list[str]
        List of full paths to all directories containing .py files directly
    filelist : list[str]
        List of full paths to all .py files found

    """
    pathlist = []
    filelist = []
    for root, _none1, files in walk(searchpath):
        contains_py = False
        for filename in files:
            _none2, fileext = path.splitext(filename)
            if ".py" == fileext:
                contains_py = True
                filepath = path.join(root, filename)
                filelist.append(filepath)
        if contains_py:
            pathlist.append(root)
    return pathlist, filelist


def check_modified(filepath: str, timestr: str) -> bool:
    """Check if a file was modified since a certain date and time.

    Parameters
    ----------
    filepath : str
        Full path of file to check
    timestr : str
        String of time to check against, formatted as "%d-%m-%y %H:%M:%S"

    Returns
    -------
    bool
        True if the file has been modified since the timestring.

    """
    if not path.exists(filepath):
        return False
    checktime = datetime.strptime(timestr, "%d-%m-%y %H:%M:%S")
    checkstamp = datetime.timestamp(checktime)
    editstamp = path.getmtime(filepath)
    return editstamp > checkstamp


def check_modified_since_docs(searchpath: str, logpath: str) -> bool:
    """Check if any python files in nested directory were modified since
    html documents were created.

    Parameters
    ----------
    logpath : str
        Full path of previous log file output by cleandoc
    htmlpath : str
        Full path to directory containing previously generated html docs

    Returns
    -------
    bool
        True if modifed since doc creation

    """
    _none, filelist = find_pyfiles(searchpath)
    regex_docs = r"(\d\d-\d\d-\d\d \d\d:\d\d:\d\d).*Docs Location: (.*)"
    results_docs = findall_infile(regex_docs, logpath, skip_exist=True)
    if len(results_docs) == 0:
        return True
    doctime = results_docs[0][0]
    for filepath in filelist:
        if check_modified(filepath, doctime):
            return True
    return False


def findall_infile(regex: str, filepath: str, skip_exist: bool = False) -> list:
    """Open ascii file for reading and get results of re.findall

    Parameters
    ----------
    regex : str
        Regular expression
    filepath : str
        Path of ascii text file to search
    skip_exist : bool
        True to skip searching through a file that doesnt exist

    Returns
    -------
    list
        Results from re.findall function
    """
    if (not path.exists(filepath)) and skip_exist:
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            filetext = file.read()
    except UnicodeDecodeError as error:
        raise IOError from error
    results = findall(regex, filetext)
    return results


def get_clean_pyfiles(logpath: str) -> list[str]:
    """Get a list of already cleaned .py files from previous cleandoc run so
    cleaning functions can be skipped.

    Parameters
    ----------
    logpath : str
        Full path of previous log file output by cleandoc
    Returns
    -------
    list[str]
        List of .py files in nested directory which are still clean
    """
    clean_pyfiles = []
    regex = r"(\d\d-\d\d-\d\d \d\d:\d\d:\d\d).*File is Clean: (.*)"
    results = findall_infile(regex, logpath, skip_exist=True)
    for result in results:
        if not check_modified(result[1], result[0]):
            clean_pyfiles.append(result[1])
    return clean_pyfiles


def config_log(logpath: str, logname: str = "cleandoc"):
    """Configure log file using logging module

    Parameters
    ----------
    logpath : str
        Path of cleandoc log file to create
    logname : str
        Name for logger

    Returns
    -------
    logger object

    """
    if logging.getLogger(logname).hasHandlers():
        return logging.getLogger(logname)
    if path.exists(logpath):
        remove(logpath)
    logging.basicConfig(
        filename=logpath,
        filemode="a",
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%d-%m-%y %H:%M:%S",
        level=logging.INFO,
    )
    logger = logging.getLogger(logname)
    logger.addHandler(logging.StreamHandler(stdout))
    return logger


# if __name__ == "__main__":
