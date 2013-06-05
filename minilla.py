# 
# Mozilla Firefox OS Gaia distribution configuration tool
#
# minilla is a monster named from Ultraman gaia http://en.wikipedia.org/wiki/Minilla
#

from bottle import route, run, template, request
import preload

@route('/')
def index():
	page = """
	Enter icon URL:
	<form method="post" action="/">
	  <input type="text" name="iconuri">
	  <input type="submit" value="Convert" />
	</form>
	"""
	return template(page)

@route('/', method='post')
def icon_convertion():
    iconuri = request.forms.get('iconuri')
    
    page = """
	icon base64:
	<img src="{{iconuri}}"/>
	<form>
	  <textarea cols=80 rows=20>{{base}}</textarea>
	</form>
	"""
    if iconuri.startswith('http'):
    	result = preload.fetch_icon_from_url(iconuri)
        print result.replace('/', '\/')
    return template(page, dict(iconuri = iconuri, base = result.replace('/', '\/')))

run(host='localhost', port=8000)