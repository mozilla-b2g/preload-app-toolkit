%rebase main
<style>
  input{
    width:320px;
    margin:10px;
  }
  button{
    margin:10px;
  }
</style>
<div id="form">
  <input type="text" value="" placeholder="enter title" id="site_title"><br/>
  <input type="text" value="" placeholder="enter uri" id="site_uri"><br/>
  <input type="text" value="" placeholder="enter iconuri" id="site_icon"><br/>
  <button id="send">save</button>
  <button id="download">download</button>
</div>
<ul id="content">
</ul>
<script>
'use strict';

var siteTitle = document.getElementById('site_title');
var siteUri = document.getElementById('site_uri');
var siteIcon = document.getElementById('site_icon');
var send = document.getElementById('send');
var download = document.getElementById('download');

function bookMarkItem (title, uri, iconUri) {
	this.title = trim(title);
  this.uri = trim(uri);
  this.iconUri = trim(iconUri);
};

var bookMarkManager = {
  get content() {
		return document.getElementById('content');
  },
	
	bookMarksList : [],
  
  addItem : function bmm_addItem(item) {

		if (!this.checkDedupe(item)) {
			this.bookMarksList.push(item);
			var newNode = this.genItem(item);
    }
		this.updateList();
  },

  removeItem : function bmm_removeItem(index) {
		this.bookMarksList.splice(index, 1);
  },

  checkDedupe : function bmm_checkDedupe(item) {
		var dedupe = false;
		this.bookMarksList.forEach(function(name) {
			if (name.uri === item.uri) {
				name.title = item.title;
				name.iconUri = item.iconUri;
				dedupe = true;
				return dedupe;
			}
		}, this);

		return dedupe;
	},

	updateList : function bmm_updateList () {
		this.content.innerHTML = "";
		this.bookMarksList.forEach(function(name){
			var newNode = this.genItem(name);
			this.content.appendChild(newNode);
		}, this);
  },

	genItem : function bmm_genItem(item) {
		var newNode = document.createElement("li");
		newNode.innerHTML = "<p>" + item.title + "</p>" +
											"<p>" + item.uri + "</p>" +
		                  "<p><img src='" + item.iconUri + "''>:" +
											item.iconUri + "</p>";

		return newNode;
	}
};
    
send.addEventListener('click', function(){
	var item = new bookMarkItem(siteTitle.value, siteUri.value, siteIcon.value);
  bookMarkManager.addItem(item);
	//bookMarkManager.updateList();
});

download.addEventListener('click', function(){
	if (bookMarkManager.bookMarksList.length == 0){
		bookMarkManager.content.innerHTML = "no data";
		return;
	}	
	var output = {
		"000000" : {
			"bookmarks" : bookMarkManager.bookMarksList
		}
	};
	bookMarkManager.content.innerHTML = JSON.stringify(output);
});

siteUri.addEventListener('keyup', function(){
  // set default iconUri
	siteIcon.value = this.value + "/favicon.ico";
});

function trim(stringToTrim) {
 return stringToTrim.replace(/^\s+|\s+$/g,"");
}
</script>
<!-- <script type="text/javascript" src="bookmarks.js"></script> -->