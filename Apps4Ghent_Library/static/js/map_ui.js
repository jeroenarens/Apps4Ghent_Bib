function MapUI() { }

MapUI.prototype.applyMargins = function() {
    var leftToggler = $(".mini-submenu-left");
    var rightToggler = $(".mini-submenu-right");
    if (leftToggler.is(":visible")) {
        $("#map .ol-zoom")
                .css("margin-left", 0)
                .removeClass("zoom-top-opened-sidebar")
                .addClass("zoom-top-collapsed");
    } else {
        $("#map .ol-zoom")
                .css("margin-left", $(".sidebar-left").width())
                .removeClass("zoom-top-opened-sidebar")
                .removeClass("zoom-top-collapsed");
    }
    if (rightToggler.is(":visible")) {
        $("#map .ol-rotate")
                .css("margin-right", 0)
                .removeClass("zoom-top-opened-sidebar")
                .addClass("zoom-top-collapsed");
    } else {
        $("#map .ol-rotate")
                .css("margin-right", $(".sidebar-right").width())
                .removeClass("zoom-top-opened-sidebar")
                .removeClass("zoom-top-collapsed");
    }
}

MapUI.prototype.isConstrained = function() {
    return $("div.mid").width() == $(window).width();
}

MapUI.prototype.applyInitialUIState = function() {
    if (this.isConstrained()) {
        $(".sidebar-left .sidebar-body").fadeOut('slide');
        $(".sidebar-right .sidebar-body").fadeOut('slide');
        $('.mini-submenu-left').fadeIn();
        $('.mini-submenu-right').fadeIn();
    }
}

MapUI.prototype.getColor = function(d) {
    return d > 1000 ? '#800026' :
            d > 500 ? '#BD0026' :
                    d > 200 ? '#E31A1C' :
                            d > 100 ? '#FC4E2A' :
                                    d > 50 ? '#FD8D3C' :
                                            d > 20 ? '#FEB24C' :
                                                    d > 10 ? '#FED976' :
                                                            '#FFEDA0';
}

MapUI.prototype.style = function(feature) {
    return {
        fillColor: getColor(feature.properties.density),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

MapUI.prototype.registerSidebarHandlers = function() {
  $('.sidebar-left .slide-submenu').on('click', function () {
      var thisEl = $(this);
      thisEl.closest('.sidebar-body').fadeOut('slide', function () {
          $('.mini-submenu-left').fadeIn();
          this.applyMargins();
      });
  });

  $('.mini-submenu-left').on('click', function () {
      var thisEl = $(this);
      $('.sidebar-left .sidebar-body').toggle('slide');
      thisEl.hide();
      this.applyMargins();
  });

  $('.sidebar-right .slide-submenu').on('click', function () {
      var thisEl = $(this);
      thisEl.closest('.sidebar-body').fadeOut('slide', function () {
          $('.mini-submenu-right').fadeIn();
          this.applyMargins();
      });
  });

  $('.mini-submenu-right').on('click', function () {
      var thisEl = $(this);
      $('.sidebar-right .sidebar-body').toggle('slide');
      thisEl.hide();
      this.applyMargins();
  });

  $(window).on("resize", this.applyMargins);
  this.applyInitialUIState();
  this.applyMargins();
}

// Registers event handlers that have functionality to change between layer
MapUI.prototype.registerLayerChangeHandlers = function(Map) {
  var self = this;

  $('[data-map]').click(function(e) {
    var layer = $(this).data('map');
    Map.dataManager.setCurrentLayer(Map, layer);
  });

  // Color change handlers
  $('[data-color]').change(function(e) {
    var color = $(this).data('color');
    if (color === "lowest") {
      var newVal = hexToRgb($(this).val());
      if (self.currentColorCalculator.maxColor === newVal) return;
      self.currentColorCalculator.maxColor = newVal;
    } else if (color === "highest") {
      var newVal = hexToRgb($(this).val());
      if (self.currentColorCalculator.minColor === newVal) return;
      self.currentColorCalculator.minColor = newVal;
    } else if (color === "level") {
      var newVal = $(this).val();
      if (self.currentColorCalculator.numberOfColors === newVal) return;
      self.currentColorCalculator.numberOfColors = newVal;
    }

    self.refreshLegend();
    Map.redrawLayers();
  });
};

MapUI.prototype.changeLayer = function(Map, layer) {
  Map.map.addLayer(Map.layers.loadingLayer);

  // Reset all layers
  Map.map.removeLayer(Map.layers.sectionsLayer);
  Map.map.removeLayer(Map.layers.wijkLayer);
  Map.map.removeLayer(Map.layers.lenersLayer);
  Map.map.removeLayer(Map.layers.borrowingsLayer);
  Map.map.removeLayer(Map.layers.librariesLayer);

  switch(layer) {
  case 'empty':
    Map.map.removeLayer(Map.layers.loadingLayer);
    Map.map.addLayer(Map.layers.sectionsLayer);
    break;
  case 'borrowersPerArea':
    MapStyle.borrowersPerAreaColorCalculator.update(calculateBorrowersPerArea(Map.dataManager));
    this.refreshLegend(Map, MapStyle.borrowersPerAreaColorCalculator);
    Map.map.removeLayer(Map.layers.loadingLayer);

    Map.map.addLayer(Map.layers.lenersLayer);
    Map.map.addLayer(Map.layers.sectionsLayer);
    break;
  case 'borrowingsPerBorrowers':
    Map.dataManager.updateBorrowingsCount(function() {
      MapStyle.borrowingsPerBorrowersColorCalculator.update(calculateBorrowingsPerBorrowers(Map.dataManager));
      this.refreshLegend(Map, MapStyle.borrowingsPerBorrowersColorCalculator);
      if (Map.dataManager.selectedSector) this.refreshInfoBox(Map, Map.dataManager.selectedSector);
      Map.map.removeLayer(Map.layers.loadingLayer);
      Map.map.addLayer(Map.layers.borrowingsLayer);
      Map.map.addLayer(Map.layers.sectionsLayer);
    }.bind(this));
    break;
  case 'libraries':
    Map.map.removeLayer(Map.layers.loadingLayer);
    Map.map.addLayer(Map.layers.sectionsLayer);
    Map.map.addLayer(Map.layers.librariesLayer);
  }
};

MapUI.prototype.registerFilterHandlers = function(Map) {
  $('[data-filter]').change(function(event) {
    Map.dataManager.setFilter(Map, $(this).data('filter'), $(this).val());
  });
};

MapUI.prototype.refreshLegend = function(Map, colorCalculator) {
  colorCalculator = colorCalculator || this.currentColorCalculator;

  // Update the color selector
  if (this.currentColorCalculator !== colorCalculator) {
    this.currentColorCalculator = colorCalculator;
    $('[data-color=lowest]').val(rgbToHex(colorCalculator.maxColor));
    $('[data-color=highest]').val(rgbToHex(colorCalculator.minColor));
    $('[data-color=level]').val(colorCalculator.numberOfColors);
  }

  var table = $('#legendTable');

  // Clear the table
  table.html('');

  // Add rows to the table one by one
  for (var i=0; i < colorCalculator.numberOfColors; ++i) {
    var value = colorCalculator.getValue(i);
    var percentValue = (value - colorCalculator.minValue) / (colorCalculator.maxValue - colorCalculator.minValue);
    var color = colorCalculator.getRgbaColor(value-0.0001, 1);

    var row = $('<tr><td><div style="width: 30px; height: 20px; background: ' + color + ';"></div><td style="padding-left:10px">' + Math.round(percentValue*100) + '%</td></tr>');
    table.append(row);

    $('#legend-colors').css('display', 'block');
  }
};

MapUI.prototype.refreshInfoBox = function(Map, feature) {
  var self = Map;
  var nr = feature.get('wijknr');

  // Generate info to show in the right sidebar
  var info = ["Information is loading..."];

  // Total no borrowers
  if (self.dataManager.borrowersCountPerSectorNumber) {
      var borrowers =  self.dataManager.borrowersCountPerSectorNumber[nr];
      info = ["Total no. Borrowers: " + borrowers];
  }

  // Total no borrowings
  if (self.dataManager.borrowingCountsPerSectorNumber) {
      info.push("Total no. Borrowings: " + self.dataManager.borrowingCountsPerSectorNumber[nr]);
  }

  // Borrowings per library
  if (self.dataManager.sectorsPerSectorNumber && self.dataManager.borrowingCounts) {
      var sector_id = self.dataManager.sectorsPerSectorNumber[nr].id;
      var libraryInfo = [];

      self.dataManager.borrowingCounts.sort(function(a, b) {
        return b.borrowing_count - a.borrowing_count;
      }).forEach(function(count) {
          if (count.to_sector == sector_id) {
            var from_library = count.from_library || "UNKNOWN";
            if (self.dataManager.librariesPerBranchCode && self.dataManager.librariesPerBranchCode[from_library])
                from_library = self.dataManager.librariesPerBranchCode[from_library].name || from_library;
            libraryInfo.push('<td>' + from_library + '</td><td>' + count.borrowing_count + '</td>');
          }
      });

      var list = libraryInfo.map(function(el) { return "<tr>" + el + "</lr>"; }).join('');
      info.push("Borrowings per library: <table><tr><th>Library</th><th># Borrowings</th></tr>" + list + "</table>");
  }

  $('#title').html(feature.get('name'));
  $('#contentgeojson').html(
    info.map(function(el) { return '<p>' + el + '</p>' }).join('')
  );
}

MapUI.prototype.refreshUI = function(Map) {
  this.changeLayer(Map, Map.dataManager.currentLayer);
};
