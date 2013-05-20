Gaia Preload webapp generation script [![Build Status](https://travis-ci.org/yurenju/gaia-preload-app.png)](https://travis-ci.org/yurenju/gaia-preload-app)

# Why need Gaia Preload App script

Pre-bundled webapp are not the quite the same as usual webapp. 
Since Pre-bundled webapp may be seen before internet is ready, it have to store linked icon to buildin base-64 strings..., etc.

Gaia Preload App script probide a `preload.py` script that help build pre-bundled webapp from given .webapp URL.

# Usage

Find a webapp URL that want to bundled with, and run the command:

    $ python preload.py http://<webapp url>

