var map = L.map('leaflet', {
  'center': [0, 0],
  'zoom': 0,
  'layers': [
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      'attribution': 'Map data &copy; OpenStreetMap contributors'
    })
  ]
});

var polyline = new L.Polyline([]).addTo(map);

map.on('click', function(event) {

  new L.Marker(event.latlng).addTo(map);

  polyline.addLatLng(event.latlng);

});
