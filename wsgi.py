# 
# Mozilla Firefox OS Gaia distribution configuration tool
#
# minilla is a monster named from Ultraman gaia http://en.wikipedia.org/wiki/Minilla
#

from bottle import route, run, template, request, view, app
import preload
import os, glob, json

# application object required by wsgi, appfog use gunicorn with wsgi
application = app()
# setup environment
DEFAULT_EXTERNAL_APP_PATH = os.path.join("gaia-raw", "external-apps")
if not os.path.exists(DEFAULT_EXTERNAL_APP_PATH):
    os.makedirs(DEFAULT_EXTERNAL_APP_PATH)

@route('/')
@view('index')
def index():
  return dict()

# icon handler
@route('/icon')
@view('icon')
def icon_input():
    return dict()

@route('/icon', method='post')
@view('icon_out')
def icon_output():
    iconuri = request.forms.get('iconuri')
    if iconuri.startswith('http'):
    	result = preload.fetch_icon_from_url(iconuri)
        print result.replace('/', '\/')
    return {'iconuri': iconuri, 'base': result.replace('/', '\/')}


# homescreen handler
@route('/homescreen')
@view('homescreen')
def homescreen():
  return dict()

@route('/apps-available')
def apps_available():
    available = [
        x.split(os.path.sep)[1:] for x in (glob.glob(os.path.join("gaia-raw", "apps", "*"))
            + glob.glob(os.path.join("gaia-raw", "external-apps", "*"))
            + glob.glob(os.path.join("gaia-raw", "showcase_apps", "*")))
        if not x.endswith(".py")]
    print available
    return {"apps-available": available}

# generate package
@route('/customize/', method='post')
def customize():
    name = str(uuid.uuid4())
    fullpath = os.path.join("outputs", name)
    os.mkdir(fullpath)
    os.mkdir(os.path.join(fullpath, "distribution"))
    os.mkdir(os.path.join(fullpath, "external-apps"))
    homescreens_path = os.path.join(fullpath, "distribution", "homescreens.json")
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

@route('/webapp')
@view('webapp')
def webapp():
    return dict()

@route('/apps/', method='post')
def apps():
    app_url = request.forms.get('app_url')
    manifest = preload.fetch_webapp(app_url, DEFAULT_EXTERNAL_APP_PATH)
    return {'name': manifest['name']}

#bookmark manager
@route('/bookmark')
@view('bookmark')
def bookmark():
  return dict()

# run server
if __name__ == '__main__':
    run(application, host='localhost', port=8000, reloader=True)