function DataManager(apiHandler) {
  this.apiHandler = apiHandler;

  this.borrowersCountPerSectorNumber = undefined;
  this.sectorsPerId = undefined;
  this.sectorsPerSectorNumber = undefined;
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
    console.log(bcount);
    var countPerSector = [];
    bcount.forEach(function(count) {
      var sector = self.sectorsPerId[count.sector];
      countPerSector[sector.number] = count.borrower_count;
    });

    self.borrowersCountPerSectorNumber = countPerSector;
    if (callback) callback(countPerSector);
  })
};
