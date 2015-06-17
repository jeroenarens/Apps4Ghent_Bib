function ApiHandler (host, prefix) {
  this.host = host;
  this.prefix = prefix || '/api/v1/';

  // Dirty hacky value that enables us to get all results on one page, thus skipping pagination
  this._page_size = 10000000
}

ApiHandler.prototype.getUrl = function(url) {
  return this.host + this.prefix + url;
};

ApiHandler.prototype.getLibraries = function(callback) {
  $.get(this.getUrl('libraries'), {format: 'json', page_size: this._page_size}, function (data) {
    callback(data.results);
  });
};

ApiHandler.prototype.getBorrowersCount = function(options, callback) {
  // options is optional
  if (typeof(options) === "function") {
    callback = options;
    options = undefined;
  } else {
    options = $.extend({}, {format: 'json', page_size: this._page_size}, options);
  }

  $.get(this.getUrl('borrowers/count'), options, function(data) {
    callback(data.results);
  });
};

ApiHandler.prototype.getSectors = function(callback) {
  $.get(this.getUrl('sectors'), {format: 'json', page_size: this._page_size}, function(data) {
    callback(data.results);
  });
};

ApiHandler.prototype.getBorrowingsCount = function(options, callback) {
  // options is optional
  if (typeof(options) === "function") {
    callback = options;
    options = undefined;
  } else {
    options = $.extend({}, {format: 'json', page_size: this._page_size}, options);
  }

  $.get(this.getUrl('borrowed-items'), options, function(data) {
    var results = data.results;

    // Recursively fetch the next batch of data
    function getNext(next) {
      if (next == null) callback(results);
      else $.get(next, function(data) { results = results.concat(data.results); getNext(data.next); })
    }
    getNext(data.next);
  });
}
