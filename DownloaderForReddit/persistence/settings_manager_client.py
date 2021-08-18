import os
import toml
import logging

from ..utils import system_util
from ..core import const
from ..database.model_enums import *
from ..database import model_enums
from ..messaging.message import MessagePriority


class SettingsManagerClient:

    def __init__(self):
        self.logger = logging.getLogger(f'DownloaderForReddit.{__name__}')
        self.config_file_path = os.path.join(
            system_util.get_data_directory(), 'config.toml')
        self.config = None
        self.load_config_file()
        self.section_dict = {}
        self.conversion_list = []
        self.supported_videos_updated = None

        # region core
        self.last_update = self.get('core', 'last_update', const.FIRST_POST_EPOCH)

        # region Display Settings
        self.short_title_char_length = self.get(
            'display', 'short_title_char_length', 15)
        default_tooltip_display_dict = {
            'name': True,
            'download_enabled': True,
            'lock_settings': False,
            'last_download_date': False,
            'date_limit': True,
            'absolute_date_limit': False,
            'post_limit': False,
            'download_naming_method': False,
            'subreddit_save_method': False,
            'download_videos': False,
            'download_images': False,
            'download_comments': False,
            'download_comment_content': False,
            'download_nsfw': False,
            'date_added': False,
            'total_score': False,
            'post_count': True,
            'content_count': False,
            'comment_count': False
        }
        self.main_window_tooltip_display_dict = self.get('display', 'main_window_tooltip_display_dict',
                                                         default_tooltip_display_dict)
        self.countdown_view_choices = [
            'DO_NOT_SHOW', 'ONLY_WHEN_ACTIVE', 'SHOW']
        self.show_schedule_countdown = self.get(
            'display', 'show_schedule_countdown', 'ONLY_WHEN_ACTIVE')
        self.scroll_to_last_added = self.get(
            'display', 'scroll_to_last_added', True)
        self.colorize_new_reddit_objects = self.get(
            'display', 'colorize_new_reddit_objects', True)
        self.new_reddit_object_display_color = self.get(
            'display', 'new_reddit_object_display_color', [0, 175, 0])
        self.colorize_disabled_reddit_objects = self.get(
            'display', 'colorize_disabled_reddit_objects', True)
        self.disabled_reddit_object_display_color = self.get('display', 'disabled_reddit_object_display_color',
                                                             [220, 0, 0])
        self.colorize_inactive_reddit_objects = self.get(
            'display', 'colorize_inactive_reddit_objects', True)
        self.inactive_reddit_object_display_color = self.get('display', 'inactive_reddit_object_display_color',
                                                             [0, 0, 200])
        self.datetime_display_format = self.get(
            'display', 'datetime_display_format', '%m/%d/%Y %I:%M %p')
        self.date_display_format = self.get(
            'display', 'date_display_format', '%m/%d/%Y')
        # endregion

        # region Notification Defaults
        self.update_notification_level = self.get(
            'notification_defaults', 'update_notification_level', 0)
        self.ignore_update = self.get(
            'notification_defaults', 'ignore_update', None)
        self.auto_display_failed_downloads = self.get(
            'notification_defaults', 'auto_display_failed_downloads', True)
        self.display_ffmpeg_warning = self.get(
            'notification_defaults', 'display_ffmpeg_warning', True)
        self.large_post_update_warning = self.get(
            'notification_defaults', 'large_post_update_warning', True)
        self.remove_reddit_object_warning = self.get(
            'notification_defaults', 'remove_reddit_object_warning', True)
        self.remove_reddit_object_list_warning = self.get('notification_defaults', 'remove_reddit_object_list_warning',
                                                          True)
        self.ask_to_sync_moved_ro_settings = self.get(
            'notification_defaults', 'ask_to_sync_moved_ro_settings', True)
        self.check_existing_reddit_objects = self.get(
            'notification_defaults', 'check_existing_reddit_objects', True)
        self.show_system_tray_icon = self.get(
            'notification_defaults', 'show_system_tray_icon', True)
        self.show_system_tray_notifications = self.get(
            'notification_defaults', 'show_system_tray_notifications', True)
        self.tray_icon_message_display_length = self.get(
            'notification_defaults', 'tray_icon_message_display_length', 6)
        # endregion

        # region Imgur
        self.imgur_client_id = self.get('imgur', 'imgur_client_id')
        self.imgur_client_secret = self.get('imgur', 'imgur_client_secret')
        self.imgur_mashape_key = self.get('imgur', 'imgur_mashape_key')
        # endregion

        # region Main Window GUI
        main_window_geom = {
            'width': 1138,
            'height': 570,
            'x': 0,
            'y': 0
        }
        self.main_window_geom = self.get(
            'main_window_gui', 'main_window_geom', main_window_geom)
        self.horizontal_splitter_state = self.get(
            'main_window_gui', 'horizontal_splitter_state', [228, 258, 624])
        self.list_order_method = self.get(
            'main_window_gui', 'list_order_method', 'name')
        self.order_list_desc = self.get(
            'main_window_gui', 'order_list_desc', False)
        self.download_radio_state = self.get(
            'main_window_gui', 'download_radio_state', 'USER')
        # endregion

        # region Reddit Object Settings Dialog
        ro_settings_geom = {
            'width': 773,
            'height': 877,
            'x': 0,
            'y': 0
        }
        self.reddit_object_settings_dialog_geom = self.get('reddit_object_settings_dialog',
                                                           'reddit_object_settings_dialog_geom', ro_settings_geom)
        self.reddit_object_settings_dialog_splitter_state = self.get('reddit_object_settings_dialog',
                                                                     'reddit_object_settings_dialog_splitter_state',
                                                                     [181, 565])
        # endregion

    def generate_default_config(self):
        self.config = {
            'title': 'Downloader For Reddit configuration file',
            'warning': 'Users are free to change these values directly, but do so carefully.  Values that are '
                       'directly modified in this file and not through an application window may cause '
                       'unpredictable behavior (but most likely crashing) if the values entered are not accounted '
                       'for by the application.'
        }
        with open(self.config_file_path, 'w') as file:
            toml.dump(self.config, file)

    def save_all(self):
        for section, key_list in self.section_dict.items():
            for key in key_list:
                value = self.get_save_value(key)
                try:
                    self.config[section][key] = value
                except KeyError:
                    self.config[section] = {key: value}
        with open(self.config_file_path, 'w') as file:
            toml.dump(self.config, file)

    def get_save_value(self, key):
        value = getattr(self, key)
        if key in self.conversion_list:
            return value.value
        return value

    def get(self, section, key, default_value=None, converter=None):
        """
        Attempts to extract the value from the config object that is loaded from a config file.  The default value is
        returned if the key is not found in the config.
        :param section: The section that the key is located in.
        :param key: The key to the value that is needed.
        :param default_value: The value that will be returned if the key is not found in the config object.
        :param converter: Optional.  Object that should wrap the value loaded from the config file.  Since objects such
                          as ModelEnums are not able to be stored in the config file, a storable value is used instead.
                          When a container is supplied the supplied container object will be initialized with the value
                          loaded from the config file.
        :return: The value as stored in the configuration.
        """
        self.map_section(section, key)
        try:
            value = self.config[section][key]
        except KeyError:
            value = default_value
        if converter is None:
            return value
        else:
            return converter(value)

    def map_section(self, section, key):
        try:
            key_list = self.section_dict[section]
            key_list.append(key)
        except KeyError:
            self.section_dict[section] = [key]

    def convert_download_dict(self, download_dict):
        converts = {}
        for key, value in download_dict.items():
            if type(value) == str and value.startswith('<') and value.endswith('>'):
                class_name = value.split('.')[0][1:]
                n = int(value.split(':')[1].strip('>'))
                e = getattr(model_enums, class_name)(n)
                converts[key] = e
        download_dict.update(converts)
        return download_dict

    def convert_message_priority(self, priority):
        self.conversion_list.append('output_priority_level')
        return MessagePriority(priority)

    def convert_quick_filters(self, quick_filters):
        for filter_list in quick_filters.values():
            for filter_dict in filter_list:
                if 'value' not in filter_dict:
                    filter_dict['value'] = None
        return quick_filters
