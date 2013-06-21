#!/usr/bin/env python

import preload
import base64
import io
from urlparse import urlparse
import unittest
from mock import patch
from mock import MagicMock
from mock import sentinel
import logging


class PreloadTest(unittest.TestCase):

    def test_convert(self):
        test_data = 'fakedata'
        encode = base64.b64encode(test_data)
        result = preload.convert_icon(test_data, 'image/png')
        assert result == 'data:image/png;base64,' + encode

    def test_has_scheme(self):
        http_url = urlparse('http://test.com/test.png')
        absolute_path = urlparse('/test.png')
        relative_path = urlparse('test.png')
        assert preload.has_scheme(http_url) == True
        assert preload.has_scheme(absolute_path) == False
        assert preload.has_scheme(relative_path) == False

    def test_get_absolute_path(self):
        domain = 'http://test.com/'
        path = 'path-1/path-2/'
        icon1 = urlparse('test.png')
        icon2 = urlparse('/test.png')
        icon3 = urlparse('http://test.com/path-3/test.png')
        assert preload.get_absolute_url(domain, path, icon1) == \
            'http://test.com/path-1/path-2/test.png'
        assert preload.get_absolute_url(domain, path, icon2) == \
            'http://test.com/test.png'
        assert preload.get_absolute_url(domain, path, icon3) == \
            'http://test.com/path-3/test.png'

    def test_get_directory_name(self):
        assert preload.get_directory_name('test!') == 'test'
        assert preload.get_directory_name('test test') == 'testtest'
        assert preload.get_directory_name('test! test@') == 'testtest'

    def test_get_origin(self):
        assert preload.split_url(
            'http://test.com/path/test.manifest')[0] == 'http://test.com'
        assert preload.split_url(
            'http://test.com/test.manifest')[0] == 'http://test.com'

    def test_fetch_icon_for_abosulte_url(self):
        absolute_return_value = '/style/icons/128.png'
        with patch('preload.get_absolute_url', return_value=absolute_return_value):
            url = preload.fetch_icon(0, {0: ""}, None, None, None)
        assert url == absolute_return_value

    @patch('preload.get_absolute_url', return_value='http://test.com/test.png')
    @patch('preload.retrieve_from_url')
    @patch('preload.convert_icon', return_value=sentinel.base64)
    @patch('mimetypes.guess_type')
    @patch('os.remove')
    def test_fetch_icon_for_http_url(self, mock1, mock2, mock3, mock4, mock6):
        my_mock = MagicMock()
        with patch('__builtin__.open', my_mock):
            manager = my_mock.return_value.__enter__.return_value
            manager.read.return_value = 'binaryimagefile'
            icon_base64 = preload.fetch_icon('0', {'0': ""}, None, None, '')
        assert icon_base64 == sentinel.base64

    @patch('preload.fetch_icon_from_url', return_value=sentinel.from_url)
    @patch('preload.get_absolute_url', return_value='test.png')
    def test_fetch_icon_for_relative_path(self, mock1, mock2):
        assert preload.fetch_icon('0', {'0': ""}, None, None, '') == sentinel.from_url

    def test_get_working_dir(self):
        assert preload.get_appcache_manifest_dir('/abc/', 'test') == '/abc/'
        assert preload.get_appcache_manifest_dir(
            '/abc/', '/test/test.manifest') == '/test/'
        assert preload.get_appcache_manifest_dir(
            '/abc/', '/test.manifest') == '/'
        assert preload.get_appcache_manifest_dir(
            '/abc/', 'test/test.manifest') == '/abc/test/'
        assert preload.get_appcache_manifest_dir('/', 'test.manifest') == '/'
        assert preload.get_appcache_manifest_dir(
            '/', '1st/test.manifest') == '/1st/'

    def test_get_appcache_manifest(self):
        manifest = preload.get_appcache_manifest(
            'http://test.com', '/manifestdir/', 'testapp', '/test.manifest')
        assert manifest['filename'] == 'test.manifest'
        assert manifest['local_dir'] == 'testapp/cache/'
        assert manifest['local_path'] == 'testapp/cache/manifest.appcache'
        assert manifest['url'] == 'http://test.com/test.manifest'

    @patch('preload.retrieve_from_url')
    @patch('os.makedirs')
    def test_fetch_resource(self, mock2, mock1):
        preload.fetch_resource('http://test.com', '/workingdir/',
                               'local_dir/', 'test.manifest')
        mock1.assert_called_with('http://test.com/workingdir/test.manifest',
                                 'local_dir/workingdir/test.manifest')

        preload.fetch_resource('http://test.com', '/workingdir/',
                               'local_dir/', '/test.manifest')
        mock1.assert_called_with('http://test.com/test.manifest',
                                 'local_dir/test.manifest')

        preload.fetch_resource('http://test.com', '/workingdir/',
                               'local_dir/', 'a/test.manifest')
        mock1.assert_called_with('http://test.com/workingdir/a/test.manifest',
                                 'local_dir/workingdir/a/test.manifest')

        preload.fetch_resource('http://test.com', '/workingdir/',
                               'local_dir/', '/a/test.manifest')
        mock1.assert_called_with('http://test.com/a/test.manifest',
                                 'local_dir/a/test.manifest')

        preload.fetch_resource('http://test.com', '/workingdir/',
                               'local_dir/', 'http://example.com/test.manifest')
        mock1.assert_called_with('http://example.com/test.manifest',
                                 'local_dir/http://example.com/test.manifest')

        result = preload.fetch_resource('http://test.com',
                                        '/workingdir/',
                                        'local_dir/',
                                        'test/test.manifest')
        assert result == 'workingdir/test/test.manifest'

    def side_effect(*args):
        return preload.get_resource_path_and_url(args[0], args[1], args[3])[1]

    @patch('preload.fetch_resource', side_effect=side_effect)
    def test_fetch_appcache(self, mock):
        preload.set_logger_level(logging.ERROR)
        lines = [
            'CACHE MANIFEST',
            '# comment test',
            '/absolute/test_1.html',
            '/test_2.html',
            'relative/test_3.html',
            'test_4.html',
            'http://example.com/test_5.html',
            'NETWORK:',
            '*',
            'FALLBACK:',
            '/ offline.html'
        ];
        newlines = preload.fetch_appcache('http://test.com', '/remote_dir/', 'local_dir', lines)
        assert newlines[0] == 'CACHE MANIFEST'
        assert newlines[2] == 'absolute/test_1.html'
        assert newlines[3] == 'test_2.html'
        assert newlines[4] == 'remote_dir/relative/test_3.html'
        assert newlines[5] == 'remote_dir/test_4.html'
        assert newlines[6] == 'http://example.com/test_5.html'
        assert newlines[-1] == '/ offline.html'

if __name__ == "__main__":
    unittest.main()
