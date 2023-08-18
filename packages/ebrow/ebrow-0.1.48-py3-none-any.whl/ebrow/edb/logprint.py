# This Python file uses the following encoding: utf-8
from __future__ import print_function
import builtins as __builtin__
from datetime import datetime

verbose = False


def logPrintVerbose(wantVerbose: bool = False):
    global verbose
    verbose = wantVerbose


def print(*args, **kwargs):
    """
    allows to inhibit console prints() when
    --verbose switch is not specified
    :param args:
    :param kwargs:
    :return:
    """
    if verbose:
        utc = datetime.utcnow()
        __builtin__.print(utc, end=' - ')
        __builtin__.print(*args, **kwargs)

def fprint(*args, **kwargs):
    """
    allows prints on files, bypassing
    the --verbose switch
    
    :param args: 
    :param kwargs: 
    :return: 
    """
    """
    :param args: 
    :param kwargs: 
    :return: 
    """
    __builtin__.print(*args, **kwargs)