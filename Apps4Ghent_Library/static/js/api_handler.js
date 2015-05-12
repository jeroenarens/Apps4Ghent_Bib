function ApiHandler (host, prefix) {
  this.host = host;
  this.prefix = prefix || '/api/v1/';
}

ApiHandler.prototype.getUrl = function(url) {
  return this.host + this.prefix + url;
};

ApiHandler.prototype.getLibraries = function(callback) {
  $.get(this.getUrl('libraries'), {format: 'json'}, function (data) {
    callback(data.results);
  });
};

ApiHandler.prototype.getBorrowersCount = function(callback) {
  $.get(this.getUrl('borrowers/count'), {format: 'json'}, function(data) {
    callback(data.results);
  });
};

ApiHandler.prototype.getSectors = function(callback) {
  $.get(this.getUrl('sectors'), {format: 'json'}, function(data) {
    callback(data.results);
  });
};