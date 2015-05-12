function DataManager(apiHandler) {
  this.apiHandler = apiHandler;

  this.borrowersCountPerSector = undefined;
}

DataManager.prototype.updateBorrowersCountPerSector = function(callback) {
  var self = this;

  this.apiHandler.getBorrowersCount(function(bcount) {
    var countPerSector = [];
    bcount.forEach(function(count) {
      countPerSector[count.sector] = count.borrower_count;
    });

    self.borrowersCountPerSector = countPerSector;
    if (callback) callback(countPerSector);
  })
}