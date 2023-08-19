# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 23:39:06 2023

@author: jkris
"""

from math import floor, log10
from typing import Union, Any, Tuple
from subprocess import run


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


def set_default(variable: Any, default: Any):
    """
    set_default
    """
    if not variable:
        return default
    return variable


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
