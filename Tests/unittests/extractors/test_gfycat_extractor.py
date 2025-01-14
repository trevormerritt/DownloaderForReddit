from unittest.mock import patch, MagicMock

from .abstract_extractor_test import ExtractorTest
from Tests.mockobjects import mock_objects
from DownloaderForReddit.extractors.gfycat_extractor import GfycatExtractor


@patch('DownloaderForReddit.extractors.base_extractor.BaseExtractor.make_dir_path')
@patch('DownloaderForReddit.extractors.base_extractor.BaseExtractor.make_title')
@patch('DownloaderForReddit.extractors.base_extractor.BaseExtractor.filter_content')
class TestGfycatExtractor(ExtractorTest):

    @patch('requests.get')
    def test_extract_single_untagged(self, get, filter_content, make_title, make_dir_path):
        dir_url = 'https://giant.gfycat.com/KindlyElderlyCony.webm'
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'json'}
        mock_response.json.return_value = {'gfyItem': {'webmUrl': dir_url}}
        get.return_value = mock_response

        post = mock_objects.get_mock_post_gfycat(session=self.session)
        make_title.return_value = post.title
        make_dir_path.return_value = 'content_dir_path'

        ge = GfycatExtractor(post)
        ge.extract_single()
        get.assert_called_with('https://api.gfycat.com/v1/gfycats/KindlyElderlyCony', timeout=10)
        self.check_output(ge, dir_url, post)

    @patch('requests.get')
    def test_extract_single_tagged(self, get, filter_content, make_title, make_dir_path):
        dir_url = 'https://giant.gfycat.com/anchoredenchantedamericanriverotter.webm'
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'json'}
        mock_response.json.return_value = {'gfyItem': {'webmUrl': dir_url}}
        get.return_value = mock_response

        post = mock_objects.get_mock_post_gfycat_tagged(session=self.session)
        filter_content.return_value = True
        make_title.return_value = post.title
        make_dir_path.return_value = 'content_dir_path'

        ge = GfycatExtractor(post)
        ge.extract_single()
        get.assert_called_with('https://api.gfycat.com/v1/gfycats/anchoredenchantedamericanriverotter', timeout=10)
        self.check_output(ge, dir_url, post)

    def test_direct_extraction(self, filter_content, make_title, make_dir_path):
        post = mock_objects.get_mock_post_gfycat_direct(session=self.session)
        filter_content.return_value = True
        make_title.return_value = post.title
        make_dir_path.return_value = 'content_dir_path'

        ge = GfycatExtractor(post)
        ge.extract_direct_link()
        self.check_output(ge, post.url, post)

    @patch('DownloaderForReddit.extractors.gfycat_extractor.GfycatExtractor.extract_single')
    def test_extract_content_assignment_single(self, es_mock, filter_content, make_title, make_dir_path):
        ge = GfycatExtractor(mock_objects.get_mock_post_gfycat())
        ge.extract_content()
        es_mock.assert_called()

    @patch('DownloaderForReddit.extractors.gfycat_extractor.GfycatExtractor.extract_direct_link')
    def test_extract_content_assignment_direct(self, es_mock, filter_content, make_title, make_dir_path):
        post = mock_objects.get_mock_post_gfycat()
        post.url += '.webm'
        ge = GfycatExtractor(post)
        ge.extract_content()

        es_mock.assert_called()

    @patch('DownloaderForReddit.extractors.gfycat_extractor.GfycatExtractor.extract_single')
    def test_failed_connection(self, es_mock, filter_content, make_title, make_dir_path):
        es_mock.side_effect = ConnectionError()
        post = mock_objects.get_mock_post_gfycat()

        ge = GfycatExtractor(post)
        ge.extract_content()

        self.assertTrue(ge.failed_extraction)
        self.assertIsNotNone(ge.failed_extraction_message)

    @patch('DownloaderForReddit.extractors.gfycat_extractor.GfycatExtractor.get_json')
    def test_redgifs(self, get_json, filter_content, make_title, make_dir_path):
        filter_content.return_value = True
        post = mock_objects.get_mock_post_gfycat(session=self.session)
        post.url = 'https://www.redgifs.com/watch/decisivecleanfallowdeer'
        expected_output = 'https://thumbs2.redgifs.com/DecisiveCleanFallowdeer.mp4'

        get_json.return_value = {'gfyItem': {'webmUrl': expected_output}}

        make_title.return_value = post.title
        make_dir_path.return_value = 'content_dir_path'

        ge = GfycatExtractor(post)
        ge.extract_content()
        self.check_output(ge, expected_output, post)
