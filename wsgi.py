# 
# Mozilla Firefox OS Gaia distribution configuration tool
#
# minilla is a monster named from Ultraman gaia http://en.wikipedia.org/wiki/Minilla
#

from bottle import route, run, template, request, view, app, post, static_file, get
import preload
import os, glob, json

# application object required by wsgi, appfog use gunicorn with wsgi
application = app()

from optparse import OptionParser
_cmd_parser = OptionParser(usage="usage: %prog [options]")
_cmd_parser.add_option('-g', '--gaia-dir',
                       action='store', type='string', dest='GAIA_RAW_DIR',
                       default='gaia-raw',
                       help='Gaia raw data folder. Default=gaia-raw')
_cmd_parser.add_option('-d', '--distribution',
                       action='store', type='string', dest='GAIA_DISTRIBUTION_DIR',
                       default='distribution',
                       help='Distribution output folder. Default=distribution')
(_cmd_options, _cmd_args) = _cmd_parser.parse_args()

# setup environment
GAIA_RAW_DIR = _cmd_options.GAIA_RAW_DIR
GAIA_DISTRIBUTION_DIR = _cmd_options.GAIA_DISTRIBUTION_DIR
DEFAULT_EXTERNAL_APP_PATH = os.path.join(GAIA_RAW_DIR, 'external-apps')
if not os.path.exists(DEFAULT_EXTERNAL_APP_PATH):
    os.makedirs(DEFAULT_EXTERNAL_APP_PATH)
BUILD_IN_APPS = [
    ["apps", "dialer"],
    ["apps", "sms"],
    ["apps", "contacts"],
    ["apps", "browser"],
    ["apps", "camera"],
    ["apps", "gallery"],
    ["apps", "fm"],
    ["apps", "settings"],
    ["external-apps", "marketplace"],
    ["apps", "calendar"],
    ["apps", "clock"],
    ["apps", "costcontrol"],
    ["apps", "email"],
    ["apps", "music"],
    ["apps", "video"]
]

@route('/')
@view('index')
def index():
  return dict()


# icon handler
@route('/gadget/icon')
@view('icon')
def icon_input():
    return dict()

@route('/gedget/icon', method='post')
@view('icon_out')
def icon_output():
    iconuri = request.forms.get('iconuri')
    if iconuri.startswith('http'):
        result = preload.fetch_icon_from_url(iconuri)
        print result.replace('/', '\/')
    return {'iconuri': iconuri, 'base': result.replace('/', '\/')}


# webapp fetcher
@route('/gadget/webapp')
@view('webapp')
def webapp():
    return dict()

@route('/utils/apps/', method='post')
def apps():
    app_url = request.forms.get('app_url')
    manifest = preload.fetch_webapp(app_url, DEFAULT_EXTERNAL_APP_PATH)
    return {'name': manifest['name']}


# homescreen handler
@route('/gaia/homescreen')
@view('homescreen')
def homescreen():
  return dict()

def get_app_list(path=GAIA_RAW_DIR):
    return [
        x.split(os.path.sep)[1:] for x in (glob.glob(os.path.join(path, "apps", "*"))
            + glob.glob(os.path.join(path, "external-apps", "*"))
            + glob.glob(os.path.join(path, "showcase_apps", "*")))
        if not x.endswith(".py")]

@route('/utils/apps-available')
def apps_available():
    available = get_app_list()
    # available += BUILD_IN_APPS
    # print available
    return {"apps-available": available}

@route('/js/<filename>')
def server_static(filename):
    return static_file(filename, root='views/js')

@post('/config')
def set_config():
    f = open('config.json', 'w');
    f.write(json.dumps({
        'gaia_dir': request.forms.get('gaia_dir'),
        'gaia_distribution_dir': request.forms.get('gaia_distribution_dir')
    }))
    f.close()

@get('/config')
def get_config():
    f = open('config.json', 'r');
    ret = f.read();
    f.close();
    return ret;

# generate package
@route('/utils/customize/', method='post')
def customize():
    name = str(uuid.uuid4())
    fullpath = os.path.join("outputs", name)
    os.mkdir(fullpath)
    os.mkdir(os.path.join(fullpath, GAIA_DISTRIBUTION_DIR))
    os.mkdir(os.path.join(fullpath, "external-apps"))
    homescreens_path = os.path.join(fullpath, GAIA_DISTRIBUTION_DIR, "homescreens.json")
    data = request.forms.get('homescreen')
    print data
    for homescreen in data:
        for appname in homescreen:
            if appname and appname[0] == "external-apps":
                result = commands.getoutput(
                    "cd %(fullpath)s%(sep)sexternal-apps && ln -s ..%(sep)s..%(sep)s..%(sep)sexternal-apps%(sep)s%(app-name)s" % {
                        "fullpath": fullpath,
                        "sep": os.path.sep,
                        "app-name": appname[1]})
                app.logger.debug(result)
    result = commands.getoutput(
        "cd %(fullpath)s && zip -r %(name)s.zip distribution external-apps" % {
            "fullpath": fullpath, "sep": os.path.sep, "name": name})
    app.logger.debug(result)
    result = commands.getoutput(
        "mv %(fullpath)s%(sep)s%(name)s.zip outputs" % {
            "fullpath": fullpath, "sep": os.path.sep, "name": name})
    app.logger.debug(result)

    return {"profile-url": "/profiles/" + name + ".zip"}


@route('/profiles/<name>.zip')
def profiles(name):
    name = name + ".zip"
    if os.path.exists(os.path.join("outputs", name)):
        # return flask.send_from_directory("outputs", name)
        return "ready, get zip from " + name
    else:
        return "Not Found", 404


#bookmark manager
@route('/gaia/bookmark')
@view('bookmark')
def bookmark():
  return dict()

# run server
if __name__ == '__main__':
    run(application, host='localhost', port=8000, reloader=True)