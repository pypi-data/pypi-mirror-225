# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from os import path, sep, remove
from getpass import getuser
from re import findall, sub
import logging
import sphinx_rtd_theme  # pylint: disable=W0611
import sphinx  # pylint: disable=W0611
from .helper import find_pyfiles, run_capture_out, format_header


def run_sphinx_all(docpath: str, confpath: str, pkgpath: str, release: str):
    """Run 4 functions sequentially in sphinx module including run_apidoc,
    edit_conf, edit_index, and run_make. Automakes creation of sphinx html documents for
    a python package (aka nested folder structure of python modules.)

    Parameters
    ----------
    docpath : str
        Full path to directory where sphinx docs will be created
    confpath : str
        Full path to sphinx conf.py file
    pkgpath : str
        Full path to directory containing all python modules to document.
        Directory name will be used as package name.
    release : str
        Release number (version) of package
    """

    _basepath, pkgname = path.split(pkgpath)
    summary = run_quickstart(docpath, pkgname, release)
    srcpath = path.join(docpath, "source")
    pathlist, _none2 = find_pyfiles(pkgpath)
    logger = logging.getLogger("cleandoc")
    logger.debug("    pathlist: %s", pathlist)
    for pypath in pathlist:
        initpath = path.join(pypath, "__init__.py")
        if not path.exists(initpath):
            with open(initpath, "w", encoding="utf-8") as initfile:
                initfile.write("")
    summary += run_apidoc(srcpath, pkgpath)
    edit_conf(confpath, [pkgpath] + pathlist)  # basepath,
    edit_index(srcpath, pkgname)
    summary += run_make(docpath)
    if len(summary) > 0:
        raise SyntaxError(summary)


def run_quickstart(docpath: str, pkgname: str, release: str) -> str:
    """Run "sphinx-quickstart" command via subprocess and check output.
    Creates files to begin sphinx documentation.

    Parameters
    ----------
    docpath : str
        Full path to directory where sphinx docs will be created
    pkgname : str
        Name of python package to document
    release : str
        Release number (version) of package
    Returns
    -------
    str
        Shell output from "sphinx-quickstart" command
    """
    qs_args = [
        "sphinx-quickstart",
        docpath,
        "--sep",
        "-p",
        pkgname,
        "-a",
        getuser(),
        "-r",
        release,
        "-v",
        release,
        "-l",
        "English",
    ]
    logger = logging.getLogger("cleandoc")
    logger.debug(" ".join(qs_args))
    qs_out, qs_err = run_capture_out(qs_args)
    qs_str = f"{format_header('Sphinx Quickstart Output')}\n{qs_out}\n{qs_err}\n"
    if ("error" in qs_str.lower()) or ("warning" in qs_str.lower()):
        logger.info(qs_str)
        return qs_str
    return ""


def run_apidoc(srcpath: str, pkgpath: str) -> str:
    """Run "sphinx-apidoc" command via subprocess and check output.
    Creates an .rst file for each .py file found in nested directories.
    RST files can be later used to create an html page for each module.

    Parameters
    ----------
    srcpath : str
        Full path of sphinx "source" directory (created from sphinx-quickstart)
    pkgpath : str
        Full path to directory containing all python modules to document.
    Returns
    -------
    str
        Shell output from "sphinx-apidoc" command
    """
    apidoc_args = ["sphinx-apidoc", "-M", "-o", srcpath, pkgpath]
    logger = logging.getLogger("cleandoc")
    logger.debug(" ".join(apidoc_args))
    apidoc_out, apidoc_err = run_capture_out(apidoc_args)
    apidoc_str = (
        f"{format_header('Sphinx Apidoc Output')}\n{apidoc_out}\n{apidoc_err}\n"
    )
    if ("error" in apidoc_str.lower()) or ("warning" in apidoc_str.lower()):
        logger.info(apidoc_str)
        return apidoc_str
    return ""


def run_make(docpath: str) -> str:
    """Run "make html" command via subprocess and check output.
    Creates html documents from sphinx .rst files.

    Parameters
    ----------
    docpath : str
        Full path to directory where sphinx docs will be created
    Returns
    -------
    str
        Shell output from "make html" command
    """
    make_args = ["cd", f"{docpath}", "&&", "make", "html"]
    logger = logging.getLogger("cleandoc")
    logger.debug(" ".join(make_args))
    make_out, make_err = run_capture_out(make_args, shell=True)
    make_str = f"{format_header('Sphinx Make Output')}\n{make_out}\n{make_err}\n"
    if ("error" in make_str.lower()) or ("warning" in make_str.lower()):
        logger.info(make_str)
        return make_str
    return ""


def get_release(confpath: str) -> str:
    """Get the previous release number from last sphinx conf.py file.
    If no conf.py file is found, release "0.0.1" is returned.
    If previuos release is found, "0.0.+1" is returned.

    Parameters
    ----------
    confpath : str
        Full path to sphinx conf.py file

    Returns
    -------
    release : str
        Release number of package for current sphinx documentation.
    """

    if not path.exists(confpath):
        return "0.0.1"
    with open(confpath, "r", encoding="ascii") as conffile:
        conftext = conffile.readlines()
    release_found = findall(r"release = '([\d\.]*)'", "".join(conftext))
    if len(release_found) == 0:
        return "0.0.1"
    release = release_found[0]
    logger = logging.getLogger("cleandoc")
    logger.debug("    last sphinx release found: %s", release)
    release_split = release.split(".")
    release_split[2] = str(int(release_split[2]) + 1)
    release = ".".join(release_split)
    return release


def edit_conf(confpath: str, pathlist: list[str]):
    """Edit sphinx conf.py file by running add_conf_paths and then
    add_conf_settings function.

    Parameters
    ----------
    confpath : str
        Full path to sphinx conf.py file
    pathlist : list[str]
        List of full paths to add to conf.py file so all modules can be found.
    """
    with open(confpath, "r", encoding="ascii") as conffile:
        conflines_orig = conffile.readlines()
    conflines = add_conf_paths(conflines_orig, pathlist)
    conftext_orig = "".join(conflines)
    conftext = add_conf_settings(conftext_orig)
    with open(confpath, "w", encoding="ascii") as conffile:
        conffile.write(conftext)


def add_conf_paths(conflines: list[str], pathlist: list[str]):
    """Add path.insert() lines into beginning of conf.py file
    so all modules can be found by sphinx.

    Parameters
    ----------
    conflines : list[str]
        List of text file lines in conf.py file (from readlines)
    pathlist : list[str]
        List of paths to append to the system path
    Returns
    -------
    str
        conflines after inserting path.insert lines
    """
    importlines = ["from sys import path\n"]
    fixpaths = [dirpath.replace(sep, "/") for dirpath in pathlist]
    pathlines = [f'path.insert(0, "{fixpath}")\n' for fixpath in fixpaths]
    conflines_out = importlines + pathlines + conflines
    return conflines_out


def add_conf_settings(conftext: str) -> str:
    """Add extensions and Napoleon settings to sphinx conf.py file.

    Parameters
    ----------
    conftext : str
        Full text contents of sphinx conf.py file.
    Returns
    -------
    str
        Edited text contents of conf.py file.

    """
    sphinxexts = """
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
"""
    conftext = sub(r"extensions = \[\]", sphinxexts, conftext)
    conftext = sub(
        r"html_theme = 'alabaster'", "html_theme = 'sphinx_rtd_theme'", conftext
    )
    return conftext


def edit_index(srcpath: str, pkgname: str):
    """Edit index.rst file which controls the main page of html docs.

    Parameters
    ----------
    srcpath : str
        Full path of sphinx "source" directory (created from sphinx-quickstart)
    """
    add_modules = f":caption: Contents:\n    \n   {pkgname}"
    indexpath = path.join(srcpath, "index.rst")
    modulespath = path.join(srcpath, "modules.rst")
    if path.exists(modulespath):
        remove(modulespath)
    with open(indexpath, "r", encoding="ascii") as indexfile:
        indexlines = indexfile.readlines()
    indextext = "".join(indexlines)
    indextext = sub(r":caption: Contents:", add_modules, indextext)
    indextext = sub(r":maxdepth: 4", ":maxdepth: 10", indextext)
    with open(indexpath, "w", encoding="ascii") as indexfile:
        indexfile.write(indextext)


# if __name__ == "__main__":
