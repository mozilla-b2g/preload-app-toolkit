var Minilla = {
  config: null,
  currentAddingApp: null,

  init: function minilla_init() {
    var updateConfigBtn = document.getElementById('update-config');
    var updateParams = document.getElementById('update-homecreen-parameters');
    var availableApps = document.querySelectorAll('.available-app');
    var gaia = document.getElementById('homescreen-gaia-srcdirs');
    var distribution =
      document.getElementById('homescreen-distribution-srcdirs');

    if (updateConfigBtn) {
      updateConfigBtn.addEventListener('click', function() {
        var config = {};
        config['gaia_dir'] = document.getElementById('gaia_dir').value;
        config['gaia_distribution_dir'] =
          document.getElementById('gaia_distribution_dir').value;
        this.setConfig('/config', config);
      }.bind(this));
      this.getConfig('/config');
    }

    if (updateParams) {
      updateParams.addEventListener('click', function() {
        var size = document.getElementById('homescreen-size').value;
        this.updateHomescreenSize(size);
      }.bind(this));
    }

    for (var item of availableApps) {
      item.addEventListener('click', this);
    }

    this.updateHomescreenSize(document.getElementById('homescreen-size').value);

    var homescreenSave = document.getElementById('homescreen-save');
    if (homescreenSave) {
      homescreenSave.addEventListener('click', this.setHomescreen);
    }

    this.marketPlaceText = document.getElementById('marketplace-search');
    this.marketPlaceButton = document.getElementById('marketplace-search-btn');
    this.marketPlaceButton.addEventListener('click', this.searchMarketplace.bind(this));

    this.closeModal = document.getElementById('modalClose');
    this.closeModal.addEventListener('click', this.closeMarketSuggestions);
  },

  updateAvailableApps: function minilla_updateApps(gaia, distribution, cb) {
    var self = this;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/apps?gaia=' + gaia + '&distribution=' + distribution);
    xhr.send();
    xhr.onreadystatechange = function() {
      if (this.readyState === 4) {
        var apps = JSON.parse(this.responseText);
        var availableApps = document.getElementById('available-apps');
        while (availableApps.firstChild) {
          availableApps.removeChild(availableApps.firstChild);
        }

        function addApp(app, badgeType) {
          var appSpan = document.createElement('span');
          appSpan.classList.add('available-app');
          appSpan.classList.add('badge');
          appSpan.classList.add(badgeType);
          appSpan.dataset.srcdir = app[0];
          appSpan.dataset.appname = app[1];

          if (app.length == 2) {
            appSpan.textContent = app[1];
          } else {
            appSpan.dataset.startpoint = app[2];
            appSpan.textContent = app[2];
          }

          appSpan.addEventListener('click', self);
          availableApps.appendChild(appSpan);
        }
        for (var i = 0; i < apps['gaia_dir'].length; i++) {
          addApp(apps['gaia_dir'][i], 'badge-info');
        }
        for (var i = 0; i < apps['gaia_distribution_dir'].length; i++) {
          addApp(apps['gaia_distribution_dir'][i], 'badge-success');
        }

        if(cb) {
          cb();
        }
      }
    };
  },

  updateHomescreenSize: function minilla_updateHomescreenSize(size) {
    var layout = document.getElementById('homescreen-layout');
    if (layout && size) {
      var addToPage = document.getElementById('add-to-page');
      while (layout.firstChild) {
        layout.removeChild(layout.firstChild);
      }
      while (addToPage.firstChild) {
        addToPage.removeChild(addToPage.firstChild);
      }
      for (var i = 0; i < size; i++) {
        var page = document.createElement('div');
        page.id = 'page' + i;
        page.classList.add('homescreen-page');
        var radio = document.createElement('input');
        radio.setAttribute('type', 'radio');
        radio.setAttribute('name', 'page-number');
        radio.id = 'radio-' + page.id;
        var label = document.createElement('span');
        if (i === 0) {
          radio.checked = true;
        }
        label.textContent = ' ' + page.id;
        radio.value = page.id;
        addToPage.appendChild(radio);
        addToPage.appendChild(label);
        layout.appendChild(page);
      }
      var dock = document.createElement('div');
      dock.id = 'homescreen-dock';
      layout.appendChild(dock);

      var radio = document.createElement('input');
      radio.setAttribute('type', 'radio');
      radio.setAttribute('name', 'page-number');
      radio.id = 'radio-dock';
      radio.value = 'homescreen-dock';
      var label = document.createElement('span');
      label.textContent = ' dock';
      addToPage.appendChild(radio);
      addToPage.appendChild(label);
    }

    var gaia = document.getElementById('homescreen-gaia-srcdirs');
    var distribution =
      document.getElementById('homescreen-distribution-srcdirs');
    if (gaia && distribution) {
      this.updateAvailableApps(gaia.value, distribution.value);
    }
  },

  setHomescreen: function minilla_setHomescreen() {
    var size = document.getElementsByClassName('homescreen-page').length;
    var homescreen = {};
    homescreen['homescreens'] = [];
    function spanAppMap(span) {
      var appArray = [];
      appArray.push(span.dataset.srcdir);
      appArray.push(span.dataset.appname);
      if (span.dataset.startpoint) {
        appArray.push(span.dataset.startpoint);
      }
      return appArray;
    }
    if (size) {
      var dock = document.getElementById('homescreen-dock').children;
      homescreen['homescreens'].push([]);
      for (var j = 0; j < dock.length; j++) {
        homescreen['homescreens'][0].push(spanAppMap(dock.item(j)));
      }
      for (var i = 0; i < size; i++) {
        homescreen['homescreens'].push([]);
        var page = document.getElementById('page' + i).children;
        for (var j = 0; j < page.length; j++) {
          homescreen['homescreens'][i + 1].push(spanAppMap(page.item(j)));
        }
      }
    }
    var form = new FormData();
    form.append('homescreen', JSON.stringify(homescreen));
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/homescreen');
    xhr.send(form);
    xhr.onreadystatechange = function() {
      if (this.readyState === 4) {

      }
    };
  },

  getConfig: function minilla_getConfig(url) {
    var self = this;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.send();
    xhr.onreadystatechange = function() {
      if (this.readyState === 4) {
        var config = JSON.parse(this.responseText);
        document.getElementById('gaia_dir').value = config['gaia_dir'];
        document.getElementById('gaia_distribution_dir').value =
          config['gaia_distribution_dir'];
      }
    };
  },

  setConfig: function minilla_setConfig(url, config) {
    var form = new FormData();
    form.append('gaia_dir', config['gaia_dir']);
    form.append('gaia_distribution_dir', config['gaia_distribution_dir']);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url);
    xhr.send(form);
    xhr.onreadystatechange = function() {
      if (this.readyState === 4) {
        var btn = document.getElementById('update-config');
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-success');
        btn.textContent = 'Success!';
      }
    };
  },

  handleEvent: function minilla_handleEvent(evt) {
    if (evt.target.classList.contains('available-app')) {
      this.currentAddingApp = evt.target;
      var targetPage;
      var radios = document.getElementsByName('page-number');
      for (var i = 0; i < radios.length; i++) {
        if (radios.item(i).checked) {
          targetPage = radios.item(i).value;
        }
      }
      var app = document.createElement('div');
      app.id = 'app-' + evt.target.textContent;
      app.classList.add('app');
      app.textContent = evt.target.textContent;
      app.dataset.srcdir = evt.target.dataset.srcdir;
      app.dataset.appname = evt.target.dataset.appname;
      if (evt.target.dataset.startpoint) {
        app.dataset.startpoint = evt.target.dataset.startpoint;
      }
      app.addEventListener('click', this);

      document.getElementById(targetPage).appendChild(app);
    }
    if (evt.target.classList.contains('app') &&
      evt.target.parentNode.classList.contains('homescreen-page')) {
      evt.target.parentNode.removeChild(evt.target);
    }
  },

  searchMarketplace: function searchMarketplace(evt) {
    evt.preventDefault();
    var query = this.marketPlaceText.value.trim();

    $('#myModal').modal({'show': true});

    if (query.length == 0) {
      return;
    }

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/marketplace/search/' + query);
    xhr.send();
    var that = this;
    xhr.onreadystatechange = function() {
      if (this.readyState === 4) {
        var config = JSON.parse(this.responseText);
        that.displayMarketSuggestions(config);
      }
    };
  },

  closeMarketSuggestions: function closeMarketSuggestions() {
    var closeButton = document.getElementById('modalClose');
    var modalContent = document.getElementById('myModalContent');
    var modalLoading = document.getElementById('myModalLoading');
    modalLoading.classList.remove('hide');
    modalContent.innerHTML = '';
    $('#myModal').modal('hide');
  },

  displayMarketSuggestions: function displayMarketSuggestions(market) {
    // Setup the close button
    var modalContent = document.getElementById('myModalContent');
    var modalLoading = document.getElementById('myModalLoading');

    modalLoading.classList.add('hide');

    if (market.meta.total_count == 0) {
      modalContent.textContent = 'No apps found';
      return;
    }

    var ul = document.createElement('ul');
    ul.classList.add('media-list');
    market.objects.forEach(function onApp(app) {
      var template = '<li class="media">' +
        '<a class="pull-left" href="#">' +
          '<img data-manifest="' + app.manifest_url + '" class="media-object" src="' + app.icons['64'] + '">' +
        '</a>' +
        '<div class="media-body">' +
          '<h4 class="media-heading">' + app.name + '</h4>' +
          '<div class="media">' + app.description + '</div>' +
        '</div>' +
      '</li>';
      ul.innerHTML += template;
    });

    ul.addEventListener('click', this.installFromMarket.bind(this));

    modalContent.appendChild(ul);

  },

  'installFromMarket': function installFromMarket(evt) {
    var manifest = evt.target.dataset['manifest'];

    if(!manifest) {
      return;
    }

    var modalContent = document.getElementById('myModalContent');
    modalContent.innerHTML = 'Installing from ' + manifest;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/marketplace/install/' + btoa(manifest));
    xhr.send();
    var that = this;
    xhr.onreadystatechange = function() {
      if (this.readyState === 4) {
        try {
          var result = JSON.parse(this.responseText);
          if (result.ok) {
            that.updateAvailableApps('apps,external-apps', 'external-apps', 
              function onUpdated() {
                alert('Succesfully installed');
                that.closeMarketSuggestions();
              });
          } else {
            modalContent.innerHTML = 'Could not install ' + manifest;
          }
        } catch (e) {
          modalContent.innerHTML = 'Could not install ' + manifest + '(' + e + ')';
        }
      }
    };
  }
};

window.addEventListener('load', function() {
  Minilla.init();
});

