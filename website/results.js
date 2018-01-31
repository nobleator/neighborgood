// results.js
//==============================================================================
//

// Insert post request to gather data for map?
var mapData = {
                'type': 'FeatureCollection',
                'features': [{
                    'type': 'Feature',
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-77.03238901390978, 38.913188059745586]
                    },
                    "properties": {
                        "title": "Mapbox DC",
                        'description': 'This is the DC office for Mapbox, utility: ',
                        'utility': 50
                    }
                },
                {
                    'type': 'Feature',
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-122.4194, 37.7749]
                    },
                    "properties": {
                        "title": "San Francisco",
                        'description': 'This is San Francisco, utility: ',
                        'utility': 100
                    }
                }]
            }

mapboxgl.accessToken = 'pk.eyJ1Ijoibm9ibGVhdG9yIiwiYSI6ImNqOWJwcnM4eTFoZTQzM2xzaTJxZzRweWUifQ.lvkOaIDxpPdPmiz7mN5pEA';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v9',
    center: [-98.5795, 39.8283],
    zoom: 2.5
});
map.on('load', function () {
    map.addLayer({
        'id': 'NeighborGoods',
        'type': 'circle',
        'source': {
            'type': 'geojson',
            'data': mapData
        },
        'layout': {},
        'paint': {
            'circle-radius': {
                property: 'utility',
                type: 'exponential',
                stops: [
                    [10, 2],
                    [100, 20]
                ]
            },
            'circle-color': '#088',
            'circle-opacity': 0.8
        }
    });
    // Create a popup, but don't add it to the map yet.
    var popup = new mapboxgl.Popup({
        closeButton: false,
        closeOnClick: false
    });

    map.on('mouseenter', 'NeighborGoods', function(e) {
        // Change the cursor style as a UI indicator.
        map.getCanvas().style.cursor = 'pointer';

        // Populate the popup and set its coordinates
        // based on the feature found.
        popup.setLngLat(e.features[0].geometry.coordinates)
            .setHTML(e.features[0].properties.description + e.features[0].properties.utility)
            .addTo(map);
    });

    map.on('mouseleave', 'NeighborGoods', function() {
        map.getCanvas().style.cursor = '';
        popup.remove();
    });
});