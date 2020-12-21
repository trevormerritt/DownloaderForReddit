import argparse
import os

from ..version import __version__
from ..utils import system_util, injector


class CLI:

    """
    A class that allows for certain command line setup arguments.
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Run the Downloader For Reddit application with additional '
                                                          'setup options')
        self.parser.add_argument('-d', '--data', type=str,
                                 help='Specify the directory in which the application data files will be stored. '
                                      '(Must be a valid directory path)')
        self.parser.add_argument('-u', '--userpath', type=str,
                                 help='Specify the directory in which user posts will be saved. (Must be a valid '
                                      'directory path)')
        self.parser.add_argument('-s', '--subpath', type=str,
                                 help='Specify the directory in which subreddit posts will be saved. (Must be a valid '
                                      'directory path)')
        self.parser.add_argument('-v', '--version', action='store_true',
                                 help='Show the application version info and exit.')
        self.path_error_message = 'The path specified is not valid.  Please make sure this path exists and that you ' \
                                  'have write permission.'

    def parse_args(self, args):
        args = self.parser.parse_args(args)
        if args.data:
            self.set_data_directory(args.data)
        if args.userpath:
            self.set_user_download_path(args.userpath)
        if args.subpath:
            self.set_subreddit_download_path(args.subpath)
        if args.version:
            self.print_version()

    def set_data_directory(self, path):
        if os.path.isdir(path):
            system_util.DATA_DIR = path
        else:
            print(self.path_error_message)
            raise SystemExit(1)

    def set_user_download_path(self, path):
        if os.path.isdir(path):
            sm = injector.get_settings_manager()
            sm.user_save_directory = path
        else:
            print(self.path_error_message)
            raise SystemExit(1)

    def set_subreddit_download_path(self, path):
        if os.path.isdir(path):
            sm = injector.get_settings_manager()
            sm.subreddit_save_directory = path
        else:
            print(self.path_error_message)
            raise SystemExit(1)

    def print_version(self):
        print(__version__)
        raise SystemExit(0)
