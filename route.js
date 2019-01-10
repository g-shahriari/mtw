var request = new XMLHttpRequest();

request.open('GET', 'https://api.openrouteservice.org/directions?api_key=5b3ce3597851110001cf624855704328a35746098c6f6f287a22cd66&coordinates=8.34234,48.23424%7C8.34423,48.26424&profile=driving-car&preference=fastest&format=json&units=m');

request.onreadystatechange = function () {
  if (this.readyState === 4) {
    console.log('Status:', this.status);
    console.log('Headers:', this.getAllResponseHeaders());
    console.log('Body:', this.responseText);
  }
};

request.send();
