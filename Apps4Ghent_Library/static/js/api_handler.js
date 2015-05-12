function ApiHandler (host, prefix) {
  this.host = host;
  this.prefix = prefix || '/api/v1/';
}


ApiHandler.prototype.getUrl = function(url) {
  return this.host + this.prefix + url;
}

ApiHandler.prototype.getLibraries = function(callback) {
    $.get(this.getUrl('libraries'), function (data) {
        callback(data.results);
    });
}