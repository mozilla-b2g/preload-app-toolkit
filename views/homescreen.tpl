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

  <div id="marketplace-view">
    <form>
      <fieldset>
        <label for="marketplace-search">Search apps in Marketplace</label>
        <input type="text" id="marketplace-search"/>
        <button class="btn btn-primary" id="marketplace-search-btn">Search</button>
      </fieldset>
    </form>
  </div>
<!--Sidebar content-->
</div>
<!-- Modal -->
<div id="myModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-header">
    <h3 id="myModalLabel">Marketplace apps</h3>
  </div>
  <div class="modal-body">
    <div id="myModalLoading">
      <span class="icon-spin icon-refresh"></span><span>Loading ...</span>
    </div>
    <div id="myModalContent">
    </div>
  </div>
  <div class="modal-footer">
    <button id="modalClose" class="btn btn-primary" aria-hidden="true">Close</button>
  </div>
</div>
<div id="homescreen" class="span10">
  <div class="row"><div id="homescreen-layout"></div></div>
  <button class="btn btn-primary" id="homescreen-save">Save</button>
</div>
</div>
</div>
