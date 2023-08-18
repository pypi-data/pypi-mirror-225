# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from argparse import ArgumentParser


def _cli_checks(parser, args: dict):
    """Check that command line args are compatible

    Parameters
    ----------
    parser: ArgumentParser object
    args : dict
    """
    if len(args["file"]) > 0 and len(args["dir"]) > 0:
        parser.error("File and Directory were both specified. Only specify one.")
    if len(args["file"]) == 0 and len(args["dir"]) == 0:
        parser.error("Neither File or Directory were specified. Please specify one.")
    if len(args["file"]) > 0 and args["noclean"]:
        parser.error("File was specified with -noclean so nothing occured.")
    if args["noclean"] and args["nodoc"]:
        parser.error("-noclean and -nodoc options were specified so nothing occured")


def parse():
    """Run full command line process"""
    desc = "Run automated cleaning and/or documentation of python code"
    fileh = "Python (.py) file to clean"
    dirh = "Directory containing Python (.py) files to clean and/or document"
    writeh = "Flag to write changes to files in-place"
    ignoreh = "Flag to continue through warnings"
    nch = "Flag to prevent cleaning of py files"
    ndh = "Flag to prevent html doc creation"
    reh = "Release or version number of documentation (X.Y.Z)"

    parser = ArgumentParser(prog="cleandoc", description=desc)
    parser.add_argument("-file", "-f", default="", help=fileh)
    parser.add_argument("-dir", "-d", default="", help=dirh)
    parser.add_argument("-write", "-w", action="store_true", help=writeh)
    parser.add_argument("-ignore", "-i", action="store_true", help=ignoreh)
    parser.add_argument("-noclean", "-nc", action="store_true", help=nch)
    parser.add_argument("-nodoc", "-nd", action="store_true", help=ndh)
    parser.add_argument("-release", "-r", default="", help=reh)

    args = vars(parser.parse_args())
    print(f"\nCommand Line Args:\n{args}\n")
    _cli_checks(parser, args)
    return [args[key] for key in args.keys()]
