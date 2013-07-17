%rebase main
<div id="row-fluid">
  <div class="span12">
	<strong>Minilla</strong> provide a web interface to ease gaia customization/distribution. <br />

	Please refer to <a href="https://wiki.mozilla.org/B2G/MarketCustomizations">https://wiki.mozilla.org/B2G/MarketCustomizations</a> for more information.
  </div>

  <div class="span12">
  	<form>
  	  <fieldset>
  	  	<legend>Default paths</legend>
  		<label for="gaia_dir">Gaia DIR</label>
		<input type="text" id="gaia_dir" name="gaia_dir">
		<span class="help-block">specify gaia repository to get build-in app list, used for homescreen customization.</span>
		<label for="gaia_distribution_dir">Gaia Distribution DIR</label>
		<input type="text" id="gaia_distribution_dir" name="gaia_distribution_dir">
		<span class="help-block">specify distribution dir for export customization result. read dir files for further customization.</span>
		<br />
		<button id="update-config" class="btn btn-large btn-primary" type="button">Update config</button>
	  </fieldset>
	</form>
	
  </div>
</div>
