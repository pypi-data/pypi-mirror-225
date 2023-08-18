# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from os import path, mkdir, getcwd
from shutil import rmtree, copytree, copyfile
import logging
from importlib import reload
import webbrowser
from typing import Union, List
from .clean import run_black, run_pylint, run_mypy
from .doq import run_doq, check_docstrings
from . import helper as ch
from .sphinxdoc import run_sphinx_all, get_release
from . import cli

reload(logging)


def cleandoc_all(
    searchpath: str, ignore: bool = False, write: bool = True, release: str = ""
):
    """Run clean_all and gen_docs functions. Check modified files since last
    document generation to skip checking of some files. Open docs in browser
    after creation or checking.

    Parameters
    ----------
    searchpath : str
        directory of python package (nested dirs of modules)
    ignore : bool
        keyword argument passed to clean_all function
    release : str
        Version of docs formatted as "X.Y.Z" for Major, Minor, Patch
    """
    searchpath = path.abspath(searchpath)
    skiplist = ch.get_clean_pyfiles("cleandoc_log.txt")
    src_changed = ch.check_modified_since_docs(searchpath, "cleandoc_log.txt")
    ch.config_log("cleandoc_log.txt")
    summary = clean_all(searchpath, ignore=ignore, write=write, skip=skiplist)
    if len(summary) == 0 or ignore:
        mainpage = gen_docs(searchpath, changed=src_changed, release=release)
        webbrowser.open(mainpage)
    logging.shutdown()


def clean_all(
    searchpath: str,
    ignore: bool = False,
    write: bool = True,
    skip: Union[bool, List[str]] = False,
):
    """Run clean_pyfile function on all .py files in searchpath.

    Parameters
    ----------
    searchpath : str
        Directory to search in all nested folders for .py files
    ignore : bool
        True to ignore Syntax warnings found, False to raise them
    write : bool
        keyword argument passed to clean_pyfile function
    skip : Union[bool, List[str]]
        List of .py files to skip cleaning.
        Or True to find list of clean pyfiles within function.
    """
    searchpath = path.abspath(searchpath)
    if not path.isdir(searchpath):
        raise FileNotFoundError("Searchpath does not exist: " + str(searchpath))
    if skip is True:
        skip = ch.get_clean_pyfiles("cleandoc_log.txt")
    elif skip is False:
        skip = []
    pyfilelist = ch.find_pyfiles(searchpath)[1]
    logger = ch.config_log("cleandoc_log.txt")
    summary_all = ""
    for i, pyfile in enumerate(pyfilelist):
        pyname = path.split(pyfile)[1]
        if pyfile in skip:  # type: ignore
            header = f"Skipping File ({i+1}/{len(pyfilelist)}): {pyname}"
            headerstr = f"{ch.format_header(header, repeat_char='o')}\n"
            logger.info(headerstr)
            logger.info("File is Clean: %s\n", pyfile)
            continue
        header = f"Checking File ({i+1}/{len(pyfilelist)}): {pyname}"
        headerstr = f"{ch.format_header(header, repeat_char='o')}\n"
        logger.info(headerstr)
        summary = clean_pyfile(pyfile, write=write)
        if (not ignore) and (len(summary) > 0):
            logger.error("%s\n", pyfile)
            logging.shutdown()
            raise SyntaxWarning(f"{pyfile}\n{summary}")
        if len(summary) == 0:
            logger.info("File is Clean: %s\n", pyfile)
        summary_all += summary
    return summary_all


def clean_pyfile(pyfilepath: str, write: bool = True):
    """Clean a .py file by checking docstrings then running doq, black,
    pylint, and mypy.

    Parameters
    ----------
    pyfilepath : str
        Full path of python (.py) file
    Returns
    -------
    str
        Summary of all command outputs concatenated together
    """
    if not path.isfile(pyfilepath):
        raise FileNotFoundError("Pyfilepath does not exist: " + str(pyfilepath))
    ch.config_log("cleandoc_log.txt")
    pyfilepath = path.abspath(pyfilepath)
    realpath = path.realpath(pyfilepath)
    summary = check_docstrings(realpath)
    summary += run_doq(realpath, write=write)
    summary += run_black(realpath, write=write)
    summary += run_pylint(realpath)
    summary += run_mypy(realpath)
    return summary


def gen_docs(pkgpath: str, changed: bool = True, release: str = ""):
    """Auto-generate sphinx html documentation for a python package.

    Parameters
    ----------
    pkgpath : str
        Full path to directory containing all python modules to document.
        Directory name will be used as package name.
    changed : bool
        True if your source files have changed since you last created docs
    release : str
        Version of docs formatted as "X.Y.Z" for Major, Minor, Patch
    Returns
    -------
    str
        Path of index.html file, the home page of the sphinx docs
    """
    pkgpath = path.abspath(pkgpath)
    if not path.isdir(pkgpath):
        raise FileNotFoundError("Pkgpath does not exist: " + str(pkgpath))
    logger = ch.config_log("cleandoc_log.txt")
    basepath, pkgname = path.split(pkgpath)
    docs = path.join(path.split(basepath)[0], "docs")
    indexpath = path.join(docs, "index.html")
    if changed is False and path.exists(docs) and len(release) == 0:
        logger.info("%s\n", ch.format_header("Skipping Gen Docs", repeat_char="o"))
        logger.info("Docs Location: %s\n", docs)
        return indexpath
    logger.info("%s\n", ch.format_header("Gen Docs Output", repeat_char="o"))
    logger.debug("    pkgpath: %s", pkgpath)
    docpath = path.join(basepath, f"_{pkgname}_working_docs")
    confpath = path.join(docpath, "source", "conf.py")
    confpath_old = path.join(docs, "conf.txt")
    if len(release) == 0:
        release = get_release(confpath_old)
    if path.exists(docpath):
        rmtree(docpath)
    mkdir(docpath)
    run_sphinx_all(docpath, confpath, pkgpath, release)
    htmlpath = path.join(docpath, "build", "html")
    if path.exists(docs):
        rmtree(docs)
    copytree(htmlpath, docs)
    copyfile(confpath, confpath_old)
    rmtree(docpath)
    logger.info("Docs Location: %s\n", docs)
    return indexpath


def cli_main():
    """
    run main cli function
    """
    pypath, dirpath, write, ignore, noclean, nodoc, release = cli.parse()
    if len(pypath) > 0:
        clean_pyfile(pypath, write=write)
    if len(dirpath) > 0 and nodoc:
        clean_all(dirpath, write=write, ignore=ignore)
    if len(dirpath) > 0 and noclean:
        gen_docs(dirpath, release=release)
    if len(dirpath) > 0:
        cleandoc_all(dirpath, write=write, ignore=ignore, release=release)
