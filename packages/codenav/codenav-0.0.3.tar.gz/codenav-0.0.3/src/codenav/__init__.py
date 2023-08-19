# -*- coding: utf-8 -*-
"""
Web App for cleaning, searching, editing, and navigating Python code.

Created on Fri Jul 14 23:39:06 2023

@author: jkris
"""
from . import cli
from .app import serve_app


def cli_main():
    """run cli"""
    port, remote, debug = cli.parse()
    serve_app(port, remote, debug)


if __name__ == "__main__":
    serve_app(8050, False, False)
