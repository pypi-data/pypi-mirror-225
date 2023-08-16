# -*- coding: utf-8 -*-
"""
Main script executing the experiment wizard.
"""
# ----------------------------------------------------------------------------------------------------------------------
#  Copyright (c) 2022-2023. Antonio Bulgheroni.
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to the following conditions:
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#  Software.
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
#  OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ----------------------------------------------------------------------------------------------------------------------
import argparse
import ctypes
import sys
from argparse import ArgumentParser

import urllib3
from PyQt5.QtWidgets import QApplication

from expwizard.experiment_wizard import ExperimentWizard

__author__ = 'Antonio Bulgheroni'
__email__ = 'antonio.bulgheroni@gmail.com'

urllib3.disable_warnings()


def top_level_parser() -> ArgumentParser:
    """Return the main argument parser"""
    parser = ArgumentParser(
        description='''Graphical Wizard for the generation of a new or for the location of an existing
        microscopy experiment. '''
    )

    # TODO: add parser parameters

    return parser


def main_gui(cli_args: argparse.Namespace):
    """Main GUI function"""
    app = QApplication(sys.argv)
    win = ExperimentWizard(parent=None, app=app)
    win.show()

    sys.exit(app.exec())


def main():
    """The MAIN"""
    parser = top_level_parser()
    parser.prog = 'experiment-wizard'
    args = parser.parse_args(sys.argv[1:])

    myappid = u'ecjrc.experimentwizard.gui.v0.0.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    main_gui(args)


if __name__ == '__main__':
    main()
