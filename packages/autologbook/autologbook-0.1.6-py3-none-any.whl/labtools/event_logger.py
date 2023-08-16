# -*- coding: utf-8 -*-
"""
Log file system event

@author: Antonio Bulgheroni
@email: antonio.bulgheroni@ec.europa.eu

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
import logging
import sys
import time
from argparse import ArgumentParser
from pathlib import Path
import threading

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

from autologbook import autoconfig

program_name = 'event-logger'
program_version = 'v0.0.1'
autologbook_version = autoconfig.VERSION


class SlowEventLogger(LoggingEventHandler):
    def __init__(self, consumer_delay: float = 0, logger=None):
        super().__init__(logger)
        self._consumer_delay = consumer_delay

    def on_any_event(self, event):
        time.sleep(self._consumer_delay)


def argument_parser() -> ArgumentParser:
    """
    Return the argument parser object.
    """
    parser = ArgumentParser(description='Tool for monitoring file system events occurring in a specific path',
                            prog=program_name)

    # global parameters and options.
    parser.add_argument('-v', '--version', action='version',
                        version=(f'{program_name} is {program_version}. - '
                                 f'autologbook package is version {autologbook_version}.'),
                        help='Print the version number and exit.')

    parser.add_argument('path', metavar='path', type=Path, help='The path to be monitored',
                        nargs='?', default=Path.cwd())
    parser.add_argument('-r', '--recursive', default=False, action='store_true',
                        help='Monitor all path subdirectories recursively.')

    parser.add_argument('-d', '--consumer-delay', dest='delay', type=float, default=0,
                        help='Simulate the time needed by the consumer to process an event.')

    return parser


def check_threads():
    print([t.name for t in threading.enumerate()])


def main():
    """The main function"""
    cli_args = sys.argv[1:]
    parser = argument_parser()
    args = parser.parse_args(cli_args)

    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = SlowEventLogger(args.delay)
    observer = Observer()
    observer.schedule(event_handler, args.path, recursive=args.recursive)
    observer.start()
    logging.info('Monitoring folder %s' % args.path)
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
