var Minilla = {
	config: null,

	getConfig: function minilla_getConfig(url) {
		var self = this;
		var xhr = new XMLHttpRequest();
		xhr.open('GET', url);
		xhr.send();
		xhr.onreadystatechange = function() {
			if (this.readyState === 4) {
				var config = JSON.parse(this.responseText);
				document.getElementById('gaia_dir').value = config['gaia_dir'];
				document.getElementById('gaia_distribution_dir').value = config['gaia_distribution_dir'];
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
		xhr.onreadystatechange= function() {
			if (this.readyState === 4) {
				var btn = document.getElementById('update-config');
				btn.classList.remove('btn-primary');
				btn.classList.add('btn-success');
				btn.textContent = 'Success!';
			}
		}
	}
};

window.addEventListener('load', function() {
	document.getElementById('update-config').addEventListener('click', function() {
		var config = {};
		config['gaia_dir'] = document.getElementById('gaia_dir').value;
		config['gaia_distribution_dir'] = document.getElementById('gaia_distribution_dir').value;
		Minilla.setConfig('/config', config);
	});
	Minilla.getConfig('/config');
});

