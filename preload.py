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

APPCACHE_LOCAL_DEFAULT_PATH = 'cache/'
APPCACHE_LOCAL_DEFAULT_NAME = 'manifest.appcache'
APPCACHE_SUBFIX_WHITELIST = ['html', 'ico', 'css', 'js', 'png', 'jpn',
                             'gif','properties','AUTHORS','svg','json']

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


def fetch_resource(base_path, local_dir, resource_path):
    """
    fetch resource described in appcache manifest
    """
    try:
        print 'get resource ' + resource_path + '...',

        # create directories if not exist
        local_resource_path = ''.join([local_dir, resource_path])
        local_resource_dir = '/'.join(local_resource_path.split('/')[:-1])
        if not os.path.exists(local_resource_dir):
            os.makedirs(local_resource_dir)

        if not resource_path.startswith('http'):
            resource_url = os.path.join(base_path,resource_path)
        else: #pre-fetch HTTP(S) URL resources
            resource_url = resource_path

        urllib.urlretrieve(resource_url, local_resource_path)
        print 'done'
    except IOError as e:
        print 'IO failed ', e
    except urllib.URLError as e:
        print 'fetch failed ', e

def fetch_appcache(domain, appcache_path, apppath):
    """
    fetch appcache file described in manifest.webapp

    output:

    [appname]/cache/[name].appcache
    [appname]/cache/[resources] (if defined)
    """
    local_appcache_path = ''
    relative_path = ''

    # Edge case: detect if has indirect path
    # which means we have to patch the appcache file
    INDIRECT_PATH = ''
    if (appcache_path.startswith('/') and len(appcache_path.split('/')) > 2):
        INDIRECT_PATH = '/'.join(appcache_path.split('/')[1:-1])+'/'
    if INDIRECT_PATH:
        print '**with indirect path:'+INDIRECT_PATH+'**',

    try:
        # dest appcache file dir
        local_dir = os.path.join(apppath, APPCACHE_LOCAL_DEFAULT_PATH)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        origin = urlparse(domain)
        base_path = '%s://%s' % (origin.scheme, origin.netloc)
        local_appcache_path = os.path.join(local_dir, APPCACHE_LOCAL_DEFAULT_NAME)

        print 'from ' + ''.join([base_path, appcache_path])
        # absolute url
        appcache_url = ''.join([base_path, appcache_path])

        # relative url
        if(not appcache_path.startswith('/')):
            appcache_url = '/'.join(appcache_url.split('/')[:-1])

        print 'save to '+ local_appcache_path,
        urllib.urlretrieve(appcache_url, local_appcache_path)
        print ' ok'

        # retrieve resources from appcache
        with open(local_appcache_path) as fd:
            lines = fd.readlines()
            newlines = []
            for line in lines:
                if (line and line.split('.')[-1].rstrip('\n')
                             in APPCACHE_SUBFIX_WHITELIST):
                    resource_path = line.rstrip('\n')

                    mod_line = resource_path
                    if INDIRECT_PATH and not resource_path.startswith('/ '):
                        resource_path = INDIRECT_PATH + resource_path
                        mod_line = resource_path

                    # handle path in OFFLINE section
                    if resource_path.startswith('/ '):
                        # replace resource path
                        resource_path = resource_path.split(' ')[1].strip()
                        mod_line = resource_path.split(' ')[0].strip() + ' ' + resource_path.split(' ')[1].strip()

                    fetch_resource(base_path, local_dir, resource_path)
                    newlines.append(mod_line)
                else:
                    newlines.append(line)

        if INDIRECT_PATH:
            with open(local_appcache_path, 'w') as fd:
                print 'overwrite new appcache'
                fd.write('\n'.join(newlines))
    except Exception as e:
        print 'fetch failed ', e

def fetch_webapp(app_url, directory=None):
    """
    get webapp file and parse for preinstalled webapp

    output:

    [appname]/manifest.webapp
    [appname]/metadata.json
    [appname]/cache/ (if defined)
    """
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

    if 'appcache_path' in manifest:
        print 'fetching appcache...',
        fetch_appcache(domain, manifest['appcache_path'], apppath)

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
        fetch_webapp(sys.argv[1])
    else:
        # automatically read and compose customized webapp from list
        # support csv like list format with ',' separator, ex:
        #
        # Youtube,http://m.youtube.com/mozilla_youtube_webapp
        with open('list') as fd:
            while True:
                line = fd.readline()
                if (len(line.split(','))>1):
                    fetch_webapp(line.split(',')[1].rstrip('\n'))
                else:
                    break;

if __name__ == '__main__':
    main()
