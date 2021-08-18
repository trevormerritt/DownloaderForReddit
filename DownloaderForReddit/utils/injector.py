"""
Downloader for Reddit takes a list of reddit users and subreddits and downloads content posted to reddit either by the
users or on the subreddits.


Copyright (C) 2017, Kyle Hickey


This file is part of the Downloader for Reddit.

Downloader for Reddit is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Downloader for Reddit is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Downloader for Reddit.  If not, see <http://www.gnu.org/licenses/>.
"""
from queue import Queue

settings_manager = None
client_settings_manager = None
server_settings_manager = None
database_handler = None
message_queue = None
scheduler = None


def get_client_settings_manager():
    global client_settings_manager
    if client_settings_manager is None:
        from ..persistence.client_settings_manager import ClientSettingsManager


def get_server_settings_manager():
    global server_settings_manager
    if server_settings_manager is None:
        from ..persistence.server_settings_manager import ServerSettingsManager


def get_settings_manager():
    print("This needs to be removed.")


def get_database_handler():
    global database_handler
    if database_handler is None:
        from ..database.database_handler import DatabaseHandler
        database_handler = DatabaseHandler()
    return database_handler


def get_message_queue():
    global message_queue
    if message_queue is None:
        message_queue = Queue()
    return message_queue


def get_scheduler():
    global scheduler
    if scheduler is None:
        from ..scheduling.scheduler import Scheduler
        scheduler = Scheduler()
    return scheduler
