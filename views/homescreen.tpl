%rebase main
    <style>
#available {
  position: fixed;
  overflow: scroll;
  padding: 1em;
  top: 0px;
  left: 0px;
  right: 0px;
  bottom: 0px;
  background-color: white;
  visibility: hidden;
  z-index: 50;
}

#dock {
  position: absolute;
  left: 32px;
  top: 96px;
  width: 576px;
  height: 96px;
  border: 1px solid black;
}

.app {
    position: absolute;
    font-size: x-small;
    width: 64px;
    height: 64px;
    border: 1px solid black;
}

.homescreen {
  position: absolute;
  width: 338px;
  height: 417px;
  border: 1px solid black;
}

p {
  font-size: small;
}
    </style>
  </head>
  <body>
    <!--h1>Configure Gaia <button id="build">Build distribution</button></h1>
    <p>Click on an icon space to choose the app for that space.</p-->
    <div id="available">
      Choose the app for this space:
      <form id="custom-url-form">
        Packaged Manifest URL or Hosted Manifest URL:
        <input type="text" name="app_url" style="width: 300px">
        <button id="custom-url-button">
          Add custom
        </button>
      </form>
    </div>
    <script>

var core = [
  [
    ["apps", "communications", "dialer"],
    ["apps", "sms"],
    ["apps", "communications", "contacts"],
    ["apps", "browser"]
  ], [
    ["apps", "camera"],
    ["apps", "gallery"],
    ["apps", "fm"],
    ["apps", "settings"],
    ["external-apps", "marketplace"]
  ], [
    ["apps", "calendar"],
    ["apps", "clock"],
    ["apps", "costcontrol"],
    ["apps", "email"],
    ["apps", "music"],
    ["apps", "video"]
  ]
];

var getEl = document.getElementById.bind(document),
    create = document.createElement.bind(document),
    txt = document.createTextNode.bind(document);

var apps = [];

var positions = [[], ["16px", "212px"], ["384px", "212px"]];

var apps_chosen = [
  new Array(20),
  new Array(20),
  new Array(20),
  new Array(20)];

var app_chosen = function () {};

window.onload = function() {
  var x = new XMLHttpRequest();
  x.open("GET", "/utils/apps-available");
  x.send();
  x.onreadystatechange = function() {
    if (this.readyState === 4) {
      apps = JSON.parse(this.responseText)['apps-available'];
      startup();
    }
  }
}

function startup() {
  var div = getEl("available"),
      ul = create("ul"),
      custom_url_form = getEl("custom-url-form");

  custom_url_form.onsubmit = function() {
    var submit_button = getEl("custom-url-button");
    submit_button.disabled = true;
    submit_button.textContent = "Downloading..."

    console.log(this.url.value);
    var x = new XMLHttpRequest();
    x.open("POST", "/utils/apps/");
    x.send(this.url.value);
    x.onreadystatechange = function() {
      if (this.readyState === 4) {
        if (this.status === 200) {
          submit_button.disabled = false;
          submit_button.textContent = "Add custom";
          custom_url_form.url.value = "";
          var parsed = JSON.parse(this.responseText);
          app_chosen(["external-apps", parsed.name]);
        }
      }
    };
    return false;
  }
  for (var ai = 0; ai < apps.length; ai++) {
    var li = create("li"),
        a = create("a");
    var split = apps[ai];
    a.textContent = split[split.length - 1];
    a.href = "#" + apps[ai].join("/").replace(" ", "+");
    a.onclick = (function(full, myname){
      return function() {
        console.log(myname);
        app_chosen(full);
        return false;
      }
    })(apps[ai], split[split.length - 1]);
    li.appendChild(a);
    ul.appendChild(li);
  }
  var li = create("li"),
      a = create("a");
  a.textContent = "Cancel";
  a.href = "#cancel";
  a.onclick = function(e) {
    getEl("available").style.visibility = "hidden";
    return;
  }
  li.appendChild(a);
  ul.appendChild(li);
  div.appendChild(ul);

  var dock = create("div");
  dock.setAttribute("id", "dock");

  for (var x = 0; x < 7; x++) {
    var app = create("div");
    app.setAttribute("class", "app");
    app.style.left = 64 * x + 16 * (x + 1) + "px";
    app.style.top = "16px";
    console.log(core[0][x]);
    if (core[0][x] !== undefined) {
      console.log(core[0][x][core[0][x].length - 1]);
      apps_chosen[0][x] = core[0][x];
      app.textContent = core[0][x][core[0][x].length - 1];
    }

    app.onclick = (function(me, myx) {
      return function(e) {
        app_chosen = function(chosen) {
          getEl("available").style.visibility = "hidden";
          me.textContent = chosen[chosen.length - 1];
          console.log("CHOSE", myx, chosen);
          apps_chosen[0][myx] = chosen;
        }
        getEl("available").style.visibility = "visible";

        console.log(myx);
        return false;
      }
    })(app, x);

    dock.appendChild(app);
  }
  document.body.appendChild(dock);


  for (var i = 1; i < 3; i++) {
    var homescreen = create("div");
    homescreen.setAttribute("class", "homescreen");

    homescreen.style.left = positions[i][0];
    homescreen.style.top = positions[i][1];

    for (var j = 0; j < 20; j++) {
      var app = create("div"),
          x = j % 4,
          y = Math.floor(j / 4);

      app.setAttribute("class", "app");
      app.style.left = x * 64 + (16 * (x + 1)) + "px";
      app.style.top = y * 64 + (16 * (y + 1)) + "px";
      if (core[i][j] !== undefined) {
        console.log(core[i][j][core[i][j].length - 1]);
        apps_chosen[i][j] = core[i][j];
        app.textContent = core[i][j][core[i][j].length - 1];
      }

      app.onclick = (function(me, myh, myx, myy) {
        return function(e) {
          app_chosen = function(chosen) {
            getEl("available").style.visibility = "hidden";
            me.textContent = chosen[chosen.length - 1];
            console.log("CHOSE", myh, myx, myy, chosen);
            apps_chosen[myh][myy * 4 + myx] = chosen;
          }
          getEl("available").style.visibility = "visible";

          console.log(myh, myx, myy);
          return false;
        }
      })(app, i, x, y);

      homescreen.appendChild(app);
    }
    document.body.appendChild(homescreen);
  }
}

/*var build = getEl("build");

build.onclick = function(e) {
  var txt = JSON.stringify({"homescreens": apps_chosen}),
      url = "/utils/customize/",
      x = new XMLHttpRequest();

  build.disabled = true;
  build.textContent = "Building..."

  x.open("POST", url);
  x.setRequestHeader("Content-Type", "application/json")
  x.send(txt);
  x.onreadystatechange = function() {
    if (this.readyState === 4) {
      if (this.status === 200) {
        build.disabled = false;
        build.textContent = "Build distribution";
        console.log(this.responseText);
        window.location = JSON.parse(this.responseText)['profile-url'];
      }
    }
  }
}*/
    </script>
