# Gaia Preload webapp generation script [![Build Status](https://travis-ci.org/yurenju/gaia-preload-app.png)](https://travis-ci.org/yurenju/gaia-preload-app)

## Why need Gaia Preload App script

Pre-bundled webapp are not quite the same as usual webapp, since Pre-bundled webapp may be seen before internet is ready.
It have to store linked icon to buildin base-64 strings,
provide correspondent matadata.json, prefetched appcache..., etc.

Gaia Preload App script provide a `preload.py` script that help build pre-bundled webapp from a given .webapp URL.

## Usage

### fetch a single webapp

Find a webapp URL that want to bundled with, and run the command:

    $ python preload.py http://<webapp url>

It will generate a folder with target webapp name.

### batch process to fetch multiple webapp

You can form a `list` file that batched the process. The format is


    Facebook,http://fa....
    Twitter,https://twi....

Put `preload.py` script with `list` file in the same folder, then run the command:

    $ python preload.py

`preload.py` script will parse the `list` file and do the conversion for you.

### convert web icon to base64 string

fetch icon from URL and convert it to base64 string

    $ python preload.py --icon http://<icon url>

## Setup unit test
```shell
$ virtualenv .env
$ source .env/bin/activate
$ pip install mock
$ python preload_test.py
```

# Experimental: Minilla web UI

We'd developing the Minilla web UI that help people ease the customization work with web interface.

The Minilla only depends on python, so you can run

    $ python wsgi.py

open browser to http://localhost:8000 and use it.
