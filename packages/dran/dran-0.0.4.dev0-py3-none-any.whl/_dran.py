#!/usr/bin/python
# =========================================================================== #
# -*- coding: utf-8 -*-                                                       #
# Project : HartRAO's 26m telescope data reduction and analysis program.      #
# File    : dran.py                                                           #
# Author  : Pfesesani V. van Zyl                                              # 
# Date    : 01/01/2016                                                        #
# Version : 1.0                                                               #
# =========================================================================== #

# Standard library imports
# --------------------------------------------------------------------------- #

import os
from sys import argv, stderr, exit
import argparse
import warnings
from _gui import GUI

# handle/ignore python warnings
def fxn():
    warnings.warn("deprecated", DeprecationWarning)

# Local imports
# --------------------------------------------------------------------------- #


def main():
    """
    Command line interface for dran.
    
    Loads the command name and parameters from :py:data:'argv'.
    """

    # command_type = HelpCommand

    # if len(argv) > 1:
    #     command_name = argv[1]

    #     try:
    #         command_type = registered_commands[command_name]
    #     except KeyError:
    #         if command_name not in ('-h', '--help'):
    #             stderr.write('Unknown command {}\n'.format(command_name))
    #         pass

    # command = command_type()
    # return command.run(**command.configure(argv[2:]))

    print("Hello DRAN")