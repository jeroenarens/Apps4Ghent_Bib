var MapStyle = {

  normalStyle: ol.style.Style({
      stroke: new ol.style.Stroke({
          color: '#800026',
          width: 5
      }),
      fill: new ol.style.Fill({
          color: '#BD0026'
      }),
      zIndex: 2
  }),

  // A text style for the labels of the statistical sectors is defined now
  normalTextStyle: {
      font: '12px Calibri,sans-serif',
      textAlign: 'center',
      offsetY: -15,
      fill: new ol.style.Fill({
          color: [0, 0, 0, 1]
      }),
      stroke: new ol.style.Stroke({
          color: [255, 255, 255, 1],
          width: 4
      })
  },

  // When the mouse would hover over a statistical sector, the style defined beneath will be used
  highlightStyle: new ol.style.Style({
      stroke: new ol.style.Stroke({
          color: [255, 0, 0, 0.6],
          width: 2
      }),
      fill: new ol.style.Fill({
          color: [255, 0, 0, 0.2]
      }),
      zIndex: 1
  }),

  highlightStyle2: new ol.style.Style({
      fill: new ol.style.Fill({
          color: [255, 0, 0, 1]
      }),
      zIndex: 50
  }),

  borrowersPerAreaColorCalculator: new ColorCalculator([255, 237, 160], [128, 0, 38],  10),

  styleFunctionBorrowersPerArea: function(feature, resolution) {
    var number = feature.get('wijknr');
    var borrowersPerArea = dataManager.borrowersCountPerSectorNumber[number] / dataManager.sectorsPerSectorNumber[number].area;
    var color = MapStyle.borrowersPerAreaColorCalculator.getRgbaColor(borrowersPerArea, 0.6);

    var style = new ol.style.Style({
        fill: new ol.style.Fill({
            color: color,
            opacity: 0.6
        })
    });
    return [style]
  },

  borrowingsPerBorrowersColorCalculator: new ColorCalculator([255, 237, 200], [100, 20, 60], 20),

  styleFunctionBorrowingsPerBorrowers: function(feature, resolution) {
    var number = feature.get('wijknr');
    var borrowingsPerBorrower = dataManager.borrowingCountsPerSectorNumber[number] / dataManager.borrowersCountPerSectorNumber[number];
    var color = MapStyle.borrowingsPerBorrowersColorCalculator.getRgbaColor(borrowingsPerBorrower, 0.6);

    var style = new ol.style.Style({
        fill: new ol.style.Fill({
            color: color,
            opacity: 0.6
        })
    });
    return [style]
  },

  // Style function for loading sections
  styleFunctionLoad: function(feature, resolution) {
    var style = new ol.style.Style({
      fill: new ol.style.Fill({
        color: [0,0,0,0.8],
      }),
      stroke: new ol.style.Stroke({
        color: [255,255,255,0.6],
      }),
      text: new ol.style.Text({
        text: 'Loading...',
        font: '12px Calibri,sans-serif',
        fill: new ol.style.Fill({color: [255,255,255,1]})
      })
    });

    return [style];
  },

  //This is the style function, a function is used to make it more dynamic/flexible
  styleFunction: function(feature, resolution) {
      var style;
      var geom = feature.getGeometry();
      if (geom.getType() == 'Point') {
          var text = feature.get('text');
          MapStyle.normalTextStyle.text = text;
          style = new ol.style.Style({
              text: new ol.style.Text(MapStyle.normalTextStyle),
              zIndex: 2
          });
      }
      else {
          style = MapStyle.highlightStyle;
      }
      return [style];
  },

  // Style function for libraries
  styleFunctionLibraries: function(feature, resolution) {
      var iconStyle = new ol.style.Style({
          image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
              anchor: [0.5, 46],
              anchorXUnits: 'fraction',
              anchorYUnits: 'pixels',
              opacity: 1,
              src: '../static/img/library_marker.png'
          }))
      });
      return [iconStyle];
  }

};
