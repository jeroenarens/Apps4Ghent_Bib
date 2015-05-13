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
