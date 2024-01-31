import sys
from io import BytesIO
import requests
from PIL import Image


# python search.py Москва, ул. Ак. Королева, 12
def search_org(toponym, org='аптека'):
    address_ll = ','.join(toponym["Point"]["pos"].split())
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        "apikey": api_key,
        "text": org,
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        sys.exit()

    json_response = response.json()
    organization = json_response["features"]
    return organization


