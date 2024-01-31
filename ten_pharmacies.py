from search_organization import search_org
import sys
from io import BytesIO
import requests
from PIL import Image

toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    sys.exit()

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
address_ll = ','.join(toponym["Point"]["pos"].split())

organizations = search_org(toponym)[:10]
points = [org["geometry"]["coordinates"] for org in organizations]
org_point = ["{0},{1}".format(point[0], point[1]) for point in points]
delta = "0.002"
pt_str = "{0},vkgrm".format(address_ll)

for i in range(10):
    hour = organizations[i]["properties"]["CompanyMetaData"].get("Hours", False)
    if hour:
        if  hour["Availabilities"][0].get("TwentyFourHours", False):
            color = 'gn'
        else:
            color = 'bl'
    else:
        color = 'gr'
    pt_str += f'~{org_point[i]},pm{color}m{i + 1}'

map_params = {
    "spn": ",".join([delta, delta]),
    "l": "map",
    "pt": pt_str
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(response.content)).show()
