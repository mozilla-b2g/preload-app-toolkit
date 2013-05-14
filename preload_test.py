#!/usr/bin/env python

import preload
import base64
import io
from urlparse import urlparse
import unittest


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
        assert preload.split_url('http://test.com/path/test.manifest')[0] == 'http://test.com'
        assert preload.split_url('http://test.com/test.manifest')[0] == 'http://test.com'


if __name__ == "__main__":
    unittest.main()


