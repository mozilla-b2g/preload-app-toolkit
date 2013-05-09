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


def convert_icon(image, mimetype):
    return 'data:%s;base64,%s' % (mimetype, base64.b64encode(image))


def has_scheme(url):
    return bool(url.scheme)


def get_absolute_url(domain, path, icon):
    icon_path = None
    origin = urlparse(''.join([domain, path]))
    if has_scheme(icon):
        return icon.geturl()
    if icon.path[0] == '/':
        icon_path = icon.path
    else:
        icon_path = '%s/%s' % (os.path.dirname(origin.path), icon.path)

    if(path.startswith('http')):
        return icon_path
    else:
        return '%s://%s%s' % (origin.scheme, origin.netloc, icon_path)


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

def fetch_icon(key, icons, domain, path, apppath):
    iconurl = get_absolute_url(domain, path,
                               urlparse(icons[key]))
    icon_base64 = '';
    if iconurl[0] == '/':
        print 'locally...'
        icon_base64 = iconurl
    #fetch icon from url
    elif (iconurl.startswith('http') and
          (iconurl.endswith(".png") or iconurl.endswith(".jpg"))):
        print key + ' from internet...',
        subfix = "/icon.png" if iconurl.endswith(".png") else "/icon.jpg"
        urllib.urlretrieve(iconurl, apppath + subfix)
        with open(apppath + subfix) as fd:
            image = fd.read()
            icon_base64 = convert_icon(image,
                                     mimetypes.guess_type(iconurl)[0])
        os.remove(apppath + subfix)
        print 'ok'
    #fetch icon from local
    else:
        image = urllib.urlopen(iconurl).read()
        icon_base64 = convert_icon(image,
                                     mimetypes.guess_type(iconurl)[0])
        print 'ok'
    return icon_base64

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
        metadata['origin'] = ''.join(['app://', appname])
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

    print 'fetching icons...'
    for key in manifest['icons']:
        manifest['icons'][key] = fetch_icon(key, manifest['icons'], domain, path, apppath)

    # add manifestURL for update
    metadata['manifestURL'] = app_url

    f = file(os.path.join(apppath, 'metadata.json'), 'w')
    f.write(json.dumps(metadata))
    f.close()

    f = codecs.open(os.path.join(apppath, manifest_filename), 'w', 'utf-8')
    f.write(json.dumps(manifest, ensure_ascii=False))
    return manifest


def main():
    if (len(sys.argv)>1):
        fetch_application(sys.argv[1])
    else:
        # automatically read and compose customized webapp from list
        # support csv like list format with ',' separator, ex:
        #
        # Youtube,http://m.youtube.com/mozilla_youtube_webapp
        with open('list') as fd:
            while True:
                line = fd.readline()
                if (len(line.split(','))>1):
                    fetch_application(line.split(',')[1].rstrip('\n'))
                else:
                    break;

if __name__ == '__main__':
    main()
