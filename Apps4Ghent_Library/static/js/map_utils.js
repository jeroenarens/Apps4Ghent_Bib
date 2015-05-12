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



