%rebase main

<div class="container-fluid">
<div class="row-fluid">
<div class="span2">
  <form>
  <fieldset>
  <label for="homescreen-size">Homescreen size</label>
  <input id="homescreen-size" name="homescreen-size" type="text" value="2">
  <p>PATH for apps in GAIA_DIR</p>
  <input type="text" id="homescreen-gaia-srcdirs" value="apps,external-apps">
  <p>PATH for apps in GAIA_DISTRIBUTION_DIR</p>
  <input type="text" id="homescreen-distribution-srcdirs" value="external-apps">
  <button id="update-homecreen-parameters" class="btn btn-primary" type="button">Update</button>
  </fieldset>
  </form>

  <p>Available apps:</p>
  <p id="available-apps">
  </p>
  <label>add to page:</label>
  <div id="add-to-page"></div>
<!--Sidebar content-->
</div>
<div id="homescreen" class="span10">
  <div class="row"><div id="homescreen-layout"></div></div>
  <button class="btn btn-primary" id="homescreen-save">Save</button>
</div>
</div>
</div>
