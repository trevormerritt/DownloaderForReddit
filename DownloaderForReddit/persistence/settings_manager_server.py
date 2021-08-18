import os
import toml
import logging

from ..utils import system_util
from ..core import const
from ..database.model_enums import *
from ..database import model_enums
from ..messaging.message import MessagePriority


class SettingsManagerServer:

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
        self.last_update = self.get(
            'core', 'last_update', const.FIRST_POST_EPOCH)
        self.current_user_list = self.get('core', 'current_user_list', None)
        self.current_subreddit_list = self.get(
            'core', 'current_subreddit_list', None)

        base_path = os.path.expanduser('~').replace('\\', '/')
        default_save_path = system_util.join_path(
            base_path, 'Downloads', 'RedditDownloads')
        self.user_save_directory = self.get(
            'core', 'user_save_directory', default_save_path)
        self.subreddit_save_directory = self.get(
            'core', 'subreddit_save_directory', default_save_path)
        self.match_file_modified_to_post_date = self.get(
            'core', 'match_file_modified_to_post_date', True)
        self.rename_invalidated_download_folders = self.get(
            'core', 'rename_invalidated_download_folders', True)
        self.invalid_rename_format = self.get(
            'core', 'invalid_rename_format', '%[dir_name](deleted)')
        self.extraction_thread_count = self.get(
            'core', 'extraction_thread_count', 4)
        self.download_thread_count = self.get(
            'core', 'download_thread_count', 4)
        self.use_multi_part_downloader = self.get(
            'core', 'use_multi_part_downloader', True)
        self.multi_part_threshold = self.get(
            'core', 'multi_part_threshold', 3 * 1024 * 1024)
        self.multi_part_chunk_size = self.get(
            'core', 'multi_part_chunk_size', 1024 * 1024)
        self.multi_part_thread_count = self.get(
            'core', 'multi_part_thread_count', 4)
        self.download_on_add = self.get('core', 'download_on_add', False)
        self.finish_incomplete_extractions_at_session_start = \
            self.get(
                'core', 'finish_incomplete_extractions_at_session_start', False)
        self.finish_incomplete_downloads_at_session_start = \
            self.get('core', 'finish_incomplete_downloads_at_session_start', False)
        self.download_reddit_hosted_videos = self.get(
            'download_defaults', 'download_reddit_hosted_videos', True)

        self.perpetual_download = self.get('core', 'perpetual_download', False)
        self.cascade_list_changes = self.get(
            'core', 'cascade_list_changes', False)
        self.reddit_access_token = self.get(
            'core', 'reddit_access_token', None)
        self.reddit_access = self.get('core', 'reddit_access', None)
        # endregion

        # region Download Defaults

        default_user_download_dict = {
            'lock_settings': False,
            'post_limit': 25,
            'post_score_limit_operator': LimitOperator.NO_LIMIT,
            'post_score_limit': 1000,
            'avoid_duplicates': True,
            'extract_self_post_links': False,
            'download_self_post_text': False,
            'self_post_file_format': 'txt',
            'comment_file_format': 'txt',
            'download_videos': True,
            'download_images': True,
            'download_gifs': True,
            'download_nsfw': NsfwFilter.INCLUDE,
            'extract_comments': CommentDownload.DO_NOT_DOWNLOAD,
            'download_comments': CommentDownload.DO_NOT_DOWNLOAD,
            'download_comment_content': CommentDownload.DO_NOT_DOWNLOAD,
            'comment_limit': 100,
            'comment_depth': 100,
            'comment_reply_limit': 100,
            'comment_score_limit': 1000,
            'comment_score_limit_operator': LimitOperator.NO_LIMIT,
            'comment_sort_method': CommentSortMethod.NEW,
            'date_limit': None,
            'post_sort_method': PostSortMethod.NEW,
            'post_download_naming_method': '%[title]',
            'comment_naming_method': '%[author_name]-comment',
            'post_save_structure': '%[author_name]',
            'comment_save_structure': '%[post_author_name]/Comments/%[post_title]',
        }

        default_subreddit_download_dict = {
            'lock_settings': False,
            'post_limit': 25,
            'post_score_limit_operator': LimitOperator.NO_LIMIT,
            'post_score_limit': 1000,
            'avoid_duplicates': True,
            'extract_self_post_links': False,
            'download_self_post_text': False,
            'self_post_file_format': 'txt',
            'comment_file_format': 'txt',
            'download_videos': True,
            'download_images': True,
            'download_gifs': True,
            'download_nsfw': NsfwFilter.INCLUDE,
            'extract_comments': CommentDownload.DO_NOT_DOWNLOAD,
            'download_comments': CommentDownload.DO_NOT_DOWNLOAD,
            'download_comment_content': CommentDownload.DO_NOT_DOWNLOAD,
            'comment_limit': 100,
            'comment_depth': 100,
            'comment_reply_limit': 100,
            'comment_score_limit': 1000,
            'comment_score_limit_operator': LimitOperator.NO_LIMIT,
            'comment_sort_method': CommentSortMethod.NEW,
            'date_limit': None,
            'post_sort_method': PostSortMethod.NEW,
            'post_download_naming_method': '%[title]',
            'comment_naming_method': '%[author_name]-comment',
            'post_save_structure': '%[subreddit_name]',
            'comment_save_structure': '%[post_subreddit_name]/Comments/%[post_title]',
        }

        self.user_download_defaults = self.get('download_defaults', 'user_download_defaults',
                                               default_user_download_dict, converter=self.convert_download_dict)
        self.subreddit_download_defaults = self.get('download_defaults', 'subreddit_download_defaults',
                                                    default_subreddit_download_dict,
                                                    converter=self.convert_download_dict)
        # endregion

        # region Output
        self.output_priority_level = self.get('output', 'output_priority_level', 2,
                                              converter=self.convert_message_priority)
        self.use_color_output = self.get('output', 'use_color_output', True)
        self.debug_color = self.get('output', 'debug_color', [0, 0, 255])
        self.info_color = self.get('output', 'info_color', [0, 0, 0])
        self.warning_color = self.get('output', 'warning_color', [255, 190, 0])
        self.error_color = self.get('output', 'error_color', [255, 125, 0])
        self.critical_color = self.get('output', 'critical_color', [255, 0, 0])
        self.requested_color = self.get('output', 'requested_color', [0, 0, 0])
        self.show_priority_level = self.get(
            'output', 'show_priority_level', True)
        self.clear_messages_on_run = self.get(
            'output', 'clear_messages_on_run', True)
        self.output_saved_content_full_path = self.get(
            'output', 'output_saved_content_full_path', False)
        # endregion

        self.datetime_display_format = self.get(
            'display', 'datetime_display_format', '%m/%d/%Y %I:%M %p')
        self.date_display_format = self.get(
            'display', 'date_display_format', '%m/%d/%Y')
        # endregion

        # region Database
        self.download_session_query_limit = self.get(
            'database', 'download_session_query_limit', 50)
        self.reddit_object_query_limit = self.get(
            'database', 'reddit_object_query_limit', 50)
        self.post_query_limit = self.get('database', 'post_query_limit', 50)
        self.content_query_limit = self.get(
            'database', 'content_query_limit', 10)
        self.comment_query_limit = self.get(
            'database', 'comment_query_limit', 60)
        # endregion

        # region Imgur
        self.imgur_client_id = self.get('imgur', 'imgur_client_id')
        self.imgur_client_secret = self.get('imgur', 'imgur_client_secret')
        self.imgur_mashape_key = self.get('imgur', 'imgur_mashape_key')
        # endregion

        # region Export
        self.export_file_path = self.get(
            'export', 'export_file_path', self.user_save_directory)
        self.export_file_type = self.get('export', 'export_file_type', 'JSON')
        self.export_nested_objects = self.get(
            'export', 'export_nested_objects', False)
        # endregion

    def load_config_file(self):
        try:
            self.config = toml.load(self.config_file_path)
        except FileNotFoundError:
            self.logger.info('No config file found.  Generating new file')
            self.generate_default_config()
        except:
            self.logger.warning('Failed to load config file', exc_info=True)
            self.generate_default_config()

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
