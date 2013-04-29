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
from zipfile import ZipFile
import shutil
import re


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
    return re.sub(r'[\W\s]', '', appname).lower()


def split_url(manifest_url):
    path = None
    url = urlparse(manifest_url)
    domain = '%s://%s' % (url.scheme, url.netloc)
    if url.path.count('/') > 1:
        path = ''.join([os.path.dirname(url.path), '/'])
    else:
        path = '/'
    return (domain, path)


def fetch_application(app_url, directory=None):
    domain, path = split_url(app_url)
    url = urlparse(app_url)
    metadata = {'origin': domain}
    manifest_filename = 'manifest.webapp'

    if url.scheme:
        print 'manifest: ' + app_url
        print 'fetching manifest...'
        manifest_url = urllib.urlopen(app_url)
        manifest = json.loads(manifest_url.read().decode('utf-8-sig'))
        metadata['installOrigin'] = domain
        if 'etag' in manifest_url.headers:
            metadata['etag'] = manifest_url.headers['etag']
    else:
        print 'extract manifest from zip...'
        appzip = ZipFile(app_url, 'r').read('manifest.webapp')
        manifest = json.loads(appzip.decode('utf-8-sig'))

    appname = get_directory_name(manifest['name'])
    manifest["shortname"] = appname
    apppath = appname
    if directory is not None:
        apppath = os.path.join(directory, appname)

    if not os.path.exists(apppath):
        os.mkdir(apppath)

    if 'package_path' in manifest or not url.scheme:
        manifest_filename = 'update.webapp'
        filename = 'application.zip'
        metadata['origin'] = 'app://%s/' % appname
        metadata['type'] = 'web'

        if url.scheme:
            print 'downloading app...'
            path = manifest['package_path']
            urllib.urlretrieve(
                manifest['package_path'],
                filename=os.path.join(apppath, filename))
            metadata['manifestURL'] = url.geturl()
            metadata['packageEtag'] = urllib.urlopen(path).headers['etag']
        else:
            print 'copying app...'
            shutil.copyfile(app_url, '%s%s%s' % (appname, os.sep, filename))
            metadata['manifestURL'] = ''.join([domain, path, 'manifest.webapp'])

        manifest['package_path'] = ''.join(['/', filename])
    else:
        print 'fetching icons...'
        for key in manifest['icons']:
            iconurl = get_absolute_url(urlparse(''.join([domain, path])),
                                       urlparse(manifest['icons'][key]))
            image = urllib.urlopen(iconurl).read()
            manifest['icons'][key] = convert(image,
                                             mimetypes.guess_type(iconurl)[0])

    f = file(os.path.join(apppath, 'metadata.json'), 'w')
    f.write(json.dumps(metadata))
    f.close()

    f = codecs.open(os.path.join(apppath, manifest_filename), 'w', 'utf-8')
    f.write(json.dumps(manifest, ensure_ascii=False))
    return manifest


def main():
    fetch_application(sys.argv[1])


if __name__ == '__main__':
    main()
