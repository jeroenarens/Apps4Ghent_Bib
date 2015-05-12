function applyMargins() {
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

function isConstrained() {
    return $("div.mid").width() == $(window).width();
}

function applyInitialUIState() {
    if (isConstrained()) {
        $(".sidebar-left .sidebar-body").fadeOut('slide');
        $(".sidebar-right .sidebar-body").fadeOut('slide');
        $('.mini-submenu-left').fadeIn();
        $('.mini-submenu-right').fadeIn();
    }
}

function getColor(d) {
    return d > 1000 ? '#800026' :
            d > 500 ? '#BD0026' :
                    d > 200 ? '#E31A1C' :
                            d > 100 ? '#FC4E2A' :
                                    d > 50 ? '#FD8D3C' :
                                            d > 20 ? '#FEB24C' :
                                                    d > 10 ? '#FED976' :
                                                            '#FFEDA0';
}

function style(feature) {
    return {
        fillColor: getColor(feature.properties.density),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function registerMapUIEventHandlers() {
  $('.sidebar-left .slide-submenu').on('click', function () {
      var thisEl = $(this);
      thisEl.closest('.sidebar-body').fadeOut('slide', function () {
          $('.mini-submenu-left').fadeIn();
          applyMargins();
      });
  });

  $('.mini-submenu-left').on('click', function () {
      var thisEl = $(this);
      $('.sidebar-left .sidebar-body').toggle('slide');
      thisEl.hide();
      applyMargins();
  });

  $('.sidebar-right .slide-submenu').on('click', function () {
      var thisEl = $(this);
      thisEl.closest('.sidebar-body').fadeOut('slide', function () {
          $('.mini-submenu-right').fadeIn();
          applyMargins();
      });
  });

  $('.mini-submenu-right').on('click', function () {
      var thisEl = $(this);
      $('.sidebar-right .sidebar-body').toggle('slide');
      thisEl.hide();
      applyMargins();
  });

  $(window).on("resize", applyMargins);
  applyInitialUIState();
  applyMargins();
}