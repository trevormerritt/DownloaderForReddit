import argparse
import os

from ..version import __version__
from ..utils import system_util, injector
from ..messaging.message import Message

"""
DFR Client
Portions of the DFR Client Parsing code that the server 
needs, but client doesn't
"""


class Client_CLI:

    """
    A class that allows for certain command line setup arguments.
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Run the Downloader For Reddit Client with additional '
                                                          'setup options')
        self.parser.add_argument('-v', '--version', action='store_true',
                                 help='Show the application version info.')

    def parse_args(self, args):
        args = self.parser.parse_args(args)
        if args.version:
            self.print_version()

    def print_version(self):
        print(__version__)
        Message.send_requested(f'Version: {__version__}')
