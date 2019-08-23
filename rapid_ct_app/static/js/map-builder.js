var mymap = L.map('map').setView([28.7041, 77.1025], 10);
L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    maxZoom: 11,
    minZoom: 10,
}).addTo(mymap);

var southWest = L.latLng(26.6958, 74.7955),
    northEast = L.latLng(30.1159, 78.8553);
var bounds = L.latLngBounds(southWest, northEast);

mymap.setMaxBounds(bounds);
mymap.on('drag', function () {
    map.panInsideBounds(bounds, {
        animate: false
    });
});

var mathura_road = L.marker([28.553892, 77.274580]).addTo(mymap);
mathura_road.bindPopup("<b>CSIR-IGIB</b><br>Mathura Road campus.").openPopup();
var mall_road = L.marker([28.698323, 77.218854]).addTo(mymap);
mall_road.bindPopup("<b>CSIR-IGIB</b><br>Mall Road campus.").openPopup();