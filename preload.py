#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib
import base64
import mimetypes
import os
import json
import codecs
from urlparse import urlparse


def convert(image, mimetype):
    return 'data:%s;base64,%s' % (mimetype, base64.b64encode(image))


def has_scheme(url):
    return bool(url.scheme)


def get_absolute_url(origin, icon):
    path = None
    if has_scheme(icon):
        return icon.geturl()
    if icon.path[0] == '/':
        path = icon.path
    else:
        path = '%s/%s' % (os.path.dirname(origin.path), icon.path)
    return '%s://%s%s' % (origin.scheme, origin.netloc, path)


def get_directory_name(appname):
    return appname.replace(' ', '').lower()


def get_origin(manifest_url):
    path = None
    url = urlparse(manifest_url)
    domain = '%s://%s' % (url.scheme, url.netloc)
    if url.path.count('/') > 1:
        path = ''.join([os.path.dirname(url.path), '/'])
    else:
        path = '/'
    return ''.join([domain, path])


def fetch_application(app_url):
    origin = get_origin(app_url)
    url = urlparse(app_url)
    metadata = {'origin': origin}
    manifest_filename = 'manifest.webapp'
    print 'manifest: ' + app_url
    print 'fetching manifest...'
    manifest_url = urllib.urlopen(app_url)
    manifest = json.loads(manifest_url.read().decode('utf-8-sig'))
    appname = get_directory_name(manifest['name'])
    if not os.path.exists(appname):
        os.mkdir(appname)

    if 'package_path' in manifest:
        manifest_filename = 'update.webapp'
        filename = 'application.zip'
        print 'downloading app...'
        urllib.urlretrieve(manifest['package_path'],
                           filename='%s%s%s' % (appname, os.sep, filename))

        metadata['origin'] = 'app://%s/' % appname
        metadata['installOrigin'] = ''.join([url.scheme, '://', url.netloc])
        metadata['type'] = 'web'
        metadata['manifestURL'] = url.geturl()
        metadata['etag'] = manifest_url.headers['etag'][1:-1]
        metadata['packageEtag'] = urllib.urlopen(manifest['package_path']).headers['etag'][1:-1]

        manifest['package_path'] = ''.join(['/', filename])
    else:
        print 'fetching icons...'
        for key in manifest['icons']:
            iconurl = get_absolute_url(urlparse(origin),
                                       urlparse(manifest['icons'][key]))
            image = urllib.urlopen(iconurl).read()
            manifest['icons'][key] = convert(image,
                                             mimetypes.guess_type(iconurl)[0])

    f = open('%s%s%s' % (appname, os.sep, 'metadata.json'), 'w')
    f.write(json.dumps(metadata))
    f.close()

    f = codecs.open('%s%s%s' % (appname, os.sep, manifest_filename), 'w', 'utf-8')
    f.write(json.dumps(manifest, ensure_ascii=False))


def main():
    fetch_application(sys.argv[1])


if __name__ == '__main__':
    main()

