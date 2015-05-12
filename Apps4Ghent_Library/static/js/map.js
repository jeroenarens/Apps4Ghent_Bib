function Map(apiHandler, mapUI, sectionsUrl) {
  this.apiHandler = apiHandler;
  this.mapUI = mapUI;

  this._generateLayers(sectionsUrl);
  this._generateView();
  this._generateMap();
  this._generateOverlays();
}

Map.prototype._generateView = function() {
  //Used to project the center of the map on the center of Ghent
  var center = ol.proj.transform([3.716667, 51.055], 'EPSG:4326', 'EPSG:3857');

  //Here, the center is used to set up the view of the map, together with a zoom variable which is arbitrarily chosen
  this.view = new ol.View({
      center: center,
      zoom: 13
  });
};

Map.prototype._generateMap = function() {
  //Now, the map is initialized. The target points to a div with id "map" in the html body.
  //The layers of the different statistical sectors are added
  this.map = new ol.Map({
      target: "map",
      layers: [this.layers.comicLayer, this.layers.sectionsLayer],
      view: this.view
  });
};

Map.prototype._generateLayers = function(sectionsUrl) {
  this.layers = {};

  this.layers.sectionsLayer = new ol.layer.Vector({
      source: new ol.source.GeoJSON({
          projection: 'EPSG:3857',
          url: sectionsUrl
      }),
      projection: 'EPSG:4326',
      style: MapStyle.normalStyle
  });

  //the layer that is used to show the different wijknr's in color
  this.layers.wijkLayer = new ol.layer.Vector({
      source: new ol.source.GeoJSON({
          projection: 'EPSG:3857',
          url: sectionsUrl
      }),
      projection: 'EPSG:4326',
      style: MapStyle.styleFunctionWijk
  });

  //the layer that is used to show the different loaners in color
  this.layers.lenersLayer = new ol.layer.Vector({
      source: new ol.source.GeoJSON({
          projection: 'EPSG:3857',
          url: sectionsUrl
      }),
      projection: 'EPSG:4326',
      style: MapStyle.styleFunctionLeners
  });

  //This is the layer beneath, which shows you a version of the map
  this.layers.comicLayer = new ol.layer.Tile({
      source: new ol.source.XYZ({
          url: 'http://api.tiles.mapbox.com/v4/mapbox.comic/{z}/{x}/{y}.png?access_token=sk.eyJ1IjoiamVyb2VuYXJlbnMiLCJhIjoiSU9zb1BIYyJ9.L1o6zaWk3EDaCi9bJf8Nug'
      })
  });

  //Other option for layer beneath from another source (open street maps)
  this.layers.layerOSM = new ol.layer.Tile({
      source: new ol.source.OSM()
  });

  //Other option for layer beneath from another source (MapQuest)
  this.layers.layerMQ = new ol.layer.Tile({
      source: new ol.source.MapQuest({
          layer: 'osm'
      })
  });

};

Map.prototype._generateOverlays = function() {
  this.overlays = {};

  //Now the overlayfeature that is defined (will be used when a mouse moves over a statistical sector
  this.overlays.featureOverlay = new ol.FeatureOverlay({
      map: this.map,
      style: MapStyle.styleFunction
  });

  this.overlays.featureOverlayWijk = new ol.FeatureOverlay({
      map: this.map,
      style: MapStyle.styleFunctionWijk
  })
};

Map.prototype.registerEventHandlers = function() {
  //Here follows the interactive part, so a movement of the mouse over a statistical sector will be noticed
  var self = this;

  this.map.on('pointermove', function (browserEvent) {
      self.overlays.featureOverlay.getFeatures().clear();
      var coordinate = browserEvent.coordinate;
      var pixel = browserEvent.pixel;


      self.map.forEachFeatureAtPixel(pixel, function (feature, layer) {
          if (!layer) {
              return;
          }
          var geometry = feature.getGeometry();
          var point;
          switch (geometry.getType()) {
              case 'MultiPolygon':
                  var poly = geometry.getPolygons().reduce(function (left, right) {
                      return left.getArea() > right.getArea() ? left : right;
                  });
                  point = poly.getInteriorPoint().getCoordinates();
                  break;
              case 'Polygon':
                  point = geometry.getInteriorPoint().getCoordinates();
                  break;
              default :
                  point = geometry.getClosestPoint(coordinate);
          }
          textFeature = new ol.Feature({
              geometry: new ol.geom.Point(point),
              // the styling function the the overlay feature, will use the name 'text' now for the text instead of 'Description'
              text: feature.get('name')
          });
          self.overlays.featureOverlay.addFeature(textFeature);
          self.overlays.featureOverlay.addFeature(feature);

      });

  });

  //functionality to let a click cursor appear when hovering over the sectionslayer
  /*
  this.map.on('pointermove', function (evt) {
      if (evt.dragging) {
          return;
      }
      var pixelOriginal = self.map.getEventPixel(evt.originalEvent);
      var hit = self.map.forEachLayerAtPixel(pixelOriginal, function (layer) {
          if (layer == self.layers.sectionsLayer) {
              return true;
          }
      });
      if (hit) self.map.getTargetElement().style.cursor = 'pointer';
  })
  */

  //functionality when a statistical sector is clicked upon
  this.map.on('singleclick', function (clickevent) {
      var coordinate = clickevent.coordinate;
      var pixel = clickevent.pixel;

      //Get the needed info and display it on the text boxes
      self.map.forEachFeatureAtPixel(pixel, function (feature, layer) {
          if (!layer) {
              return;
          }
          $('#title').html(feature.get('name'));
          $('#contentgeojson').html('<p>' + "wijk nummer: " + feature.get('wijknr') + '</p>' + '<p>' + "Aantal leners: " + feature.get('borrowers') + '</p>');
      });
  });
};

Map.prototype.drawLibraries = function() {
    var self = this;

    this.apiHandler.getLibraries(function(libraries) {
        // Gather the lat,long points from the library
        var library_coordinates = libraries.map(getLibraryLatLong);

        // Transform the coordinates
        var transformed_coordinates = library_coordinates.map(convertLatLong);

        // Turn coordinates into a list of features
        var features = transformed_coordinates.map(function(trans_coord) {
            var point = new ol.geom.Point(trans_coord);
            return new ol.Feature(point);
        });

        // Draw them on the map
        var vectorSource = new ol.source.Vector({
            features: features
        });

        self.layers.librariesLayer = new ol.layer.Vector({
            source: vectorSource
        });

        self.map.addLayer(self.layers.librariesLayer);

        self.mapUI.registerLayerChangeHandlers(self);
    });
}
