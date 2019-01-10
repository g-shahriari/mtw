

var mymap = L.map('mapid').setView([35.7125,51.3995], 16);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'sk.eyJ1IjoiZ29zaHRhc2Itc2hhaHJpYXJpIiwiYSI6ImNqcDA5N2xiMzJ0Z3AzcWtmeXBmNDB1ZGgifQ.uOkowgSJd7M1XVJuHOCONg'
}).addTo(mymap);





var popup = L.popup();

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(mymap);
}
