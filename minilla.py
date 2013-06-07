# 
# Mozilla Firefox OS Gaia distribution configuration tool
#
# minilla is a monster named from Ultraman gaia http://en.wikipedia.org/wiki/Minilla
#

from bottle import route, run, template, request, view
import preload
import os, glob, json

HEADER = """
<!DOCTYPE html>
<html lang='en'>
  <head>
    <meta charset='UTF-8'>
    <title>Let's work for the Open Web</title>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <meta name='description' content='Minilla by Mozilla Taiwan'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="dns-prefetch" href="//ajax.googleapis.com">
    <link rel="dns-prefetch" href="//netdna.bootstrapcdn.com">

    <script src='http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js'></script>
    <link href='http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.no-icons.min.css' rel='stylesheet'>
    <!--script src='http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/js/bootstrap.min.js'></script-->
    <link href='http://netdna.bootstrapcdn.com/font-awesome/3.1.1/css/font-awesome.min.css' rel='stylesheet'>
    <style>
    html, body {
	  margin: 0;
	  padding: 0;
	}
    </style>
  </head>
  <body>
    <div class="navbar navbar-inverse">
      <div class="navbar-inner">
      <a class="brand" href="/">Minilla</a>
      <ul class="nav">
      <li><a href="/homescreen">homescreen</a></li>
      <li><a href="/icon">icon convertor</a></li>
      </ul>
      </div>
    </div>
    <div class="container-fluid">
"""
FOOTER = """
    </div>
  </body>
</html>
"""

@route('/')
def index():
  page = HEADER + """
  welcome
  """ + FOOTER
  return template(page)

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

@route('/apps/', method='post')
def apps():
    app_url = request.forms.get('url')
    manifest = preload.fetch_application(app_url, "external-apps")
    return {'name': manifest['shortname']}


# run server
run(host='localhost', port=8000)