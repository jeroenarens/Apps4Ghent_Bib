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
  $('#OSM').on('click', function () {
      #
      Map.map.removeLayer(Map.layers.sectionsLayer);
      Map.map.removeLayer(Map.layers.wijkLayer);
      Map.map.removeLayer(Map.layers.lenersLayer);
      Map.map.removeLayer(Map.layers.librariesLayer);
      Map.map.addLayer(Map.layers.wijkLayer);
      Map.map.addLayer(Map.layers.sectionsLayer);
      Map.map.addLayer(Map.layers.librariesLayer);
  });

  $('#OpenStreet').on('click', function () {
      Map.map.removeLayer(Map.layers.sectionsLayer);
      Map.map.removeLayer(Map.layers.wijkLayer);
      Map.map.removeLayer(Map.layers.lenersLayer);
      Map.map.removeLayer(Map.layers.librariesLayer);
      Map.map.addLayer(Map.layers.lenersLayer);
      Map.map.addLayer(Map.layers.sectionsLayer);
      Map.map.addLayer(Map.layers.librariesLayer);
  });

  $('#MapQuest').on('click', function () {
      Map.map.removeLayer(Map.layers.sectionsLayer);
      Map.map.removeLayer(Map.layers.wijkLayer);
      Map.map.removeLayer(Map.layers.lenersLayer);
      Map.map.removeLayer(Map.layers.librariesLayer);
      Map.map.addLayer(Map.layers.wijkLayer);
      Map.map.addLayer(Map.layers.sectionsLayer);
      Map.map.addLayer(Map.layers.librariesLayer);
  });
}