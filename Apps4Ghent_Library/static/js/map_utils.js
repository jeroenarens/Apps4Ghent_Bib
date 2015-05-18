function convertLatLong(coord) {
    return ol.proj.transform(coord, 'EPSG:4326', 'EPSG:3857');
}

function getLibraryLatLong(library) {
    // TODO: I turned the lat and long around on the server
    return [
        parseFloat(library.longitude),
        parseFloat(library.latitude)
    ];
}

function calculateBorrowersPerArea(dataManager) {
    return dataManager.borrowersCountPerSectorNumber.map(function(count, snumber) {
        var area = dataManager.sectorsPerSectorNumber[snumber].area;
        if (area == 0) return 0;
        return count / area;
    });
}

function calculateBorrowingsPerBorrowers(dataManager) {
    return dataManager.borrowingCountsPerSectorNumber.map(function(count, snumber) {
      var bcount = dataManager.borrowersCountPerSectorNumber[snumber];
      if (bcount == 0) return 0;
      return count / bcount;
    });
}

function componentToHex(c) {
      var hex = c.toString(16);
      return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(rgb) {
      return "#" + componentToHex(rgb[0]) + componentToHex(rgb[1]) + componentToHex(rgb[2]);
}

function hexToRgb(hex) {
      var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result ? [
          parseInt(result[1], 16),
          parseInt(result[2], 16),
          parseInt(result[3], 16)
      ] : [0,0,0];
}
