# 
# Mozilla Firefox OS Gaia distribution configuration tool
#
# minilla is a monster named from Ultraman gaia http://en.wikipedia.org/wiki/Minilla
#

from bottle import route, run, template, request
import preload

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
      <a class="brand" href="#">Minilla</a>
      <ul class="nav">
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

@route('/icon')
def icon_input():
	page = HEADER + """
	<div id="row-fluid">
        <div class="span12">
	Enter icon URL:
	<form method="post" action="/icon">
	  <input type="text" name="iconuri">
	  <input type="submit" value="Convert" />
	</form>
	    </div>
    </div>
	""" + FOOTER
	return template(page)

@route('/icon', method='post')
def icon_output():
    iconuri = request.forms.get('iconuri')
    
    page = HEADER + """
    <div id="row-fluid">
        <div class="span12">
	icon base64:
	<img src="{{iconuri}}"/>
	<form>
	  <textarea cols=80 rows=20>{{base}}</textarea>
	</form>
	    </div>
    </div>
	""" + FOOTER
    if iconuri.startswith('http'):
    	result = preload.fetch_icon_from_url(iconuri)
        print result.replace('/', '\/')
    return template(page, dict(iconuri = iconuri, base = result.replace('/', '\/')))

run(host='localhost', port=8000)