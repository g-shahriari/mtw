from urllib2 import Request, urlopen
import json
import math
headers = {
  'Accept': 'application/json; charset=utf-8'
}

list = [9.970093,48.477473,9.207916,49.153868,37.573242,55.801281,115.663757,38.106467,115.663757,38.106467]
a =math.floor((len(list)-1)/2)
b  = '9.970093,48.477473%7C9.207916,49.153868%7C37.573242,55.801281%7C115.663757,38.106467%7C115.663757,38.106467'


request = Request('https://api.openrouteservice.org/matrix?api_key=5b3ce3597851110001cf624855704328a35746098c6f6f287a22cd66&profile=driving-car&locations='+b+'&metrics=distance', headers=headers)

response_body = json.loads(urlopen(request).read())

print response_body['distances'][0]
print a
print b
