function DataManager(mapUI, apiHandler) {
  this.mapUI = mapUI;
  this.apiHandler = apiHandler;

  this.selectedSector = undefined;
  this.currentLayer = "empty";
  this.filters = {};

  this.libraries = undefined;
  this.librariesPerBranchCode = undefined;
  this.sectorsPerId = undefined;
  this.sectorsPerSectorNumber = undefined;

  this.borrowersCountPerSectorNumber = undefined;
  this.borrowingCounts = undefined;
  this.borrowingCountsPerSectorNumber = undefined;
  this.borrowingCountsPerLibrary = undefined;

  this.clearableProperties = [
    'borrowersCountPerSectorNumber', 'borrowingCounts', 'borrowingCountsPerSectorNumber', 'borrowingCountsPerLibrary'
  ];
}

DataManager.prototype.updateSectors = function(callback) {
  var self = this;

  this.apiHandler.getSectors(function(sectors) {
    var sectorsPerId = [];
    var sectorsPerNumber = [];
    sectors.forEach(function(sector) {
      sectorsPerId[sector.id] = sector;
      sectorsPerNumber[sector.number] = sector;
    });

    self.sectorsPerId = sectorsPerId;
    self.sectorsPerSectorNumber = sectorsPerNumber;
    if (callback) callback(self.sectorsPerId, self.sectorsPerSectorNumber);
  });
};

DataManager.prototype.updateBorrowersCount = function(callback) {
  var self = this;

  this.apiHandler.getBorrowersCount(this.filters, function(bcount) {
    var countPerSector = [];
    bcount.forEach(function(count) {
      var sector = self.sectorsPerId[count.sector];
      countPerSector[sector.number] = count.borrower_count;
    });

    self.borrowersCountPerSectorNumber = countPerSector;
    if (callback) callback(countPerSector);
  })
};

DataManager.prototype.updateBorrowingsCount = function(callback) {
  var self = this;

  this.apiHandler.getBorrowingsCount(this.filters, function(bcount) {
    self.borrowingCounts = bcount;

    // Count per sector
    var borrowingCountsPerSectorNumber = [];
    bcount.forEach(function(el) {
      var snumber = self.sectorsPerId[el.to_sector].number;
      if (!!borrowingCountsPerSectorNumber[snumber])
        borrowingCountsPerSectorNumber[snumber] += el.borrowing_count;
      else
        borrowingCountsPerSectorNumber[snumber] = el.borrowing_count;
    });
    self.borrowingCountsPerSectorNumber = borrowingCountsPerSectorNumber;

    // Count per library
    var borrowingCountsPerLibrary = {};
    bcount.forEach(function(el) {
      if (!!borrowingCountsPerLibrary[el.from_library])
        borrowingCountsPerLibrary[el.from_library] += el.borrowing_count;
      else
        borrowingCountsPerLibrary[el.from_library] = el.borrowing_count;
    });
    self.borrowingCountsPerLibrary = borrowingCountsPerLibrary;

    if (callback) callback(borrowingCountsPerSectorNumber, borrowingCountsPerLibrary);
  });
};

DataManager.prototype.updateLibraries = function(callback) {
  var self = this;

  this.apiHandler.getLibraries(function(libraries) {
    librariesPerId = {};

    libraries.forEach(function(library) {
      librariesPerId[library.branch_code] = library;
    });

    self.libraries = libraries;
    self.librariesPerBranchCode = librariesPerId;
    if (callback) callback(libraries, librariesPerId);
  });
};

DataManager.prototype.setCurrentLayer = function(Map, layer) {
  if (this.currentLayer != layer) {
    this.currentLayer = layer;
    this.mapUI.changeLayer(Map, layer);
  }
};

DataManager.prototype.setSelectedSector = function(Map, sector) {
  if (this.selectedSector != sector) {
    this.selectedSector = sector;
    this.mapUI.refreshInfoBox(Map, sector);
  }
}

DataManager.prototype._clearData = function() {
  this.clearableProperties.forEach(function(prop) {
    this[prop] = undefined;
  });
}

DataManager.prototype.setFilter = function(Map, filter, value) {
  if (value === 'null') value = undefined;

  if (!!value) {
    if (this.filters[filter] != value) {
      this.filters[filter] = value;
      this._clearData();
      this.mapUI.refreshUI(Map);
    }
  } else if (this.filters[filter]) {
    delete this.filters[filter];
    this._clearData();
    this.mapUI.refreshUI(Map);
  }
};
