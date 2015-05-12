var MapStyle = {

  //The layer for where the different statistical sectors are drawn upon
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

  //the colors used for the wijknr
  getColorWijk: function(d) {
      return d > 30 ? 'rgba(128, 0, 38, 0.6)' :
              d > 25 ? 'rgba(189, 0, 38, 0.6)' :
                      d > 20 ? 'rgba(227, 26, 28, 0.6)' :
                              d > 15 ? 'rgba(252, 78, 42, 0.6)' :
                                      d > 10 ? 'rgba(253, 141, 60, 0.6)' :
                                              d > 5 ? 'rgba(254, 178, 76, 0.6)' :
                                                      d > 0 ? 'rgba(254, 217, 118, 0.6)' :
                                                              'rgba(255, 237, 160, 0.6)';
  },

  //The styling with the used wijknr
  styleFunctionWijk: function(feature, resuolution) {
      var style = new ol.style.Style({
          fill: new ol.style.Fill({
              color: MapStyle.getColorWijk(feature.get('wijknr')),
              opacity: 0.1
          })
      });
      return [style]
  },

  //the colors used for the borrowers
  getColorLeners: function(d) {
      return d > 1750 ? 'rgba(128, 0, 38, 0.6)' :
              d > 1500 ? 'rgba(189, 0, 38, 0.6)' :
                      d > 1250 ? 'rgba(227, 26, 28, 0.6)' :
                              d > 1000 ? 'rgba(252, 78, 42, 0.6)' :
                                      d > 750 ? 'rgba(253, 141, 60, 0.6)' :
                                              d > 500 ? 'rgba(254, 178, 76, 0.6)' :
                                                      d > 250 ? 'rgba(254, 217, 118, 0.6)' :
                                                              'rgba(255, 237, 160, 0.6)';
  },

  //The styling with the used wijknr
  styleFunctionLeners: function(feature, resuolution) {
      var style = new ol.style.Style({
          fill: new ol.style.Fill({
              color: MapStyle.getColorLeners(feature.get('borrowers')),
              opacity: 0.6
          })
      });
      return [style]
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
  styleFunctionlibs: function(feature, resolution) {
      var style;
      var geom = feature.getGeometry();
      style = MapStyle.highlightStyle2;
      return [style];
  }

};