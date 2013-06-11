%rebase main
<style>
  input{
    width:320px;
    margin:10px;
  }
  button{
    margin:10px;
  }
	#content li{
    padding:20px;
    width: 300px;
    list-style: none;
  }
  #content li:hover{
    cursor: pointer;
  }  
  #content li.selected{
    border:1px solid #f00;
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
			this.updateList();
		}
  },

  removeItem : function bmm_removeItem(e) {
		e.stopPropagation();
		var self = this;
		var getItem = e.target.parentNode;
		var getUri = getItem.childNodes[1].innerHTML;
		var cursor = 0;
		bookMarkManager.bookMarksList.forEach(function(name) {
			if (name.uri === getUri) {
				bookMarkManager.bookMarksList.splice(cursor, 1);
				bookMarkManager.updateList();
			}
			cursor += 1;
		}, bookMarkManager);
	},

  checkDedupe : function bmm_checkDedupe(item) {
		var dedupe = false;
		var cursor = 0;
		this.bookMarksList.forEach(function(name) {
			if (name.uri === item.uri) {
				name.title = item.title;
				name.iconUri = item.iconUri;
				dedupe = true;
				this.updateList(cursor);
				return dedupe;
			}
			cursor += 1;
		}, this);
		return dedupe;
	},

	updateList : function bmm_updateList (index) {
		if (index === undefined) {
			index = this.bookMarksList.length - 1;
		}
		this.content.innerHTML = "";
		var cursor = 0;
		this.bookMarksList.forEach(function(name){
			var newNode = this.genItem(name);
			if (cursor == index) {
				newNode.classList.add('selected');
			}
			this.content.appendChild(newNode);
			cursor += 1;
		}, this);
  },

	genItem : function bmm_genItem(item) {
		var self = this;
		var newNode = document.createElement("li");
		var closeButton =  document.createElement("button");
    closeButton.innerHTML = 'delete';
    newNode.innerHTML = "<p>" + item.title + "</p>" +
											"<p>" + item.uri + "</p>" +
											"<p><img src='" + item.iconUri + "'>:" +
		                  item.iconUri + "</p>";
		closeButton.addEventListener('click', self.removeItem.bind(self), false);
		newNode.appendChild(closeButton);
		newNode.addEventListener('click', self.editItem, false);
		return newNode;
	},

  editItem : function bmm_editItem(evt) {
		var self = evt.currentTarget;
		var getBookMarkList = self.parentNode.childNodes;
    for (var i = 0; i < getBookMarkList.length; i++){
			 getBookMarkList[i].classList.remove('selected');
		}
		self.classList.add('selected');
		siteTitle.value = self.childNodes[0].innerHTML;
		siteUri.value = self.childNodes[1].innerHTML;
		siteIcon.value = self.childNodes[2].childNodes[0].src;
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