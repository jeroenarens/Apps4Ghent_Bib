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

function getLibraries(callback) {
    $.get('http://localhost:8000/api/v1/libraries', function (data) {
        callback(data.results);
    });
}

