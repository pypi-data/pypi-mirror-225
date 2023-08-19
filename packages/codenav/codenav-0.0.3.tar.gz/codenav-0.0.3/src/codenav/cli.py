# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

from argparse import ArgumentParser


def parse():
    """Run command line parsing"""
    desc = "Web App for cleaning, searching, editing, and navigating Python code."
    porth = "Port number to host web app from"
    remoteh = (
        "Flag to host web app remotely across entire network instead (default is local)"
    )
    debugh = "Flag to turn on debug mode for web app"
    parser = ArgumentParser(prog="codenav", description=desc)
    parser.add_argument("-port", "-p", type=int, default=8050, help=porth)
    parser.add_argument("-remote", "-r", action="store_true", help=remoteh)
    parser.add_argument("-debug", "-d", action="store_true", help=debugh)
    args = vars(parser.parse_args())
    print(f"\nCommand Line Args:\n{args}\n")
    return [args[key] for key in args.keys()]
