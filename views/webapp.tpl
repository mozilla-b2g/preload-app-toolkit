%rebase main
<div id="row-fluid">
    <div class="span12">
	Enter Packaged Manifest URL or Hosted Manifest URL:
	<form method="post" action="/utils/apps/">
	  <input type="text" name="app_url">
	  <input type="submit" value="Fetch" />
	</form>
	    </div>
    </div>
    <div class="span12">
    <div id="available">
      App for this space:
    </div>
    </div>
<script>
'use strict';
window.onload = function() {
  var apps = [];
  var div = document.getElementById("available");

  var x = new XMLHttpRequest();
  x.open("GET", "/utils/apps-available");
  x.send();
  x.onreadystatechange = function() {
    if (this.readyState === 4) {
      apps = JSON.parse(this.responseText)['apps-available'];
      var ul = document.createElement('ul');
      for (var ai = 0; ai < apps.length; ai++) {
	    var li = document.createElement("li");
	    var split = apps[ai];
	    li.textContent = split[split.length - 1];
	    ul.appendChild(li);
	  }
	  div.appendChild(ul);
    }
  }
}
</script>