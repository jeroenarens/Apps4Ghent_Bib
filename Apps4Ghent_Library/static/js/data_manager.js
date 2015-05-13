function DataManager(apiHandler) {
  this.apiHandler = apiHandler;

  this.borrowersCountPerSectorNumber = undefined;
  this.sectorsPerId = undefined;
  this.sectorsPerSectorNumber = undefined;
  this.borrowingCounts = undefined;
  this.borrowingCountsPerSectorNumber = undefined;
  this.borrowingCountsPerLibrary = undefined;
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

  this.apiHandler.getBorrowersCount(function(bcount) {
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

  this.apiHandler.getBorrowingsCount(function(bcount) {
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
}
