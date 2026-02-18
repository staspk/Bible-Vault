from enum import Enum
import requests

from definitions import TEMP_OUTPUT
from kozubenko.print import print_green, print_red



# curl -X GET "https://api.scripture.api.bible/v1/bibles?language=grc&include-full-details=true" -H "accept: application/json" -H "api-key: 018c2b475ce04f75327cfa3cc29328d6"

# curl -X GET "https://api.scripture.api.bible/v1/bibles?ids=3aefb10641485092-01&include-full-details=true" -H "accept: application/json" -H "api-key: 018c2b475ce04f75327cfa3cc29328d6"

# curl -X GET "https://api.scripture.api.bible/v1/bibles/3aefb10641485092-01" -H "accept: application/json" -H "api-key: 018c2b475ce04f75327cfa3cc29328d6"


class BibleIDs(Enum):
    Greek_Textus_Receptus = '3aefb10641485092-01'



""" 
ISO 639-3
    Greek, Ancient - grc
"""

API_KEY = '018c2b475ce04f75327cfa3cc29328d6'
BASE_URL = 'https://api.scripture.api.bible/v1/bibles/'

def get_Bible():
    # URL = f'{BASE_URL}{BibleIDs.Greek_Textus_Receptus}'
    URL = "https://api.scripture.api.bible/v1/bibles/3aefb10641485092-01"
    URL = 'https://api.scripture.api.bible/v1/bibles/3aefb10641485092-01/books'
    headers = {
        "accept": "application/json",
        'api-key': API_KEY
    }
    # params = {
    #     "language": "grc",
    #     "ids": "3aefb10641485092-01",
    #     "include-full-details": "true"
    # }

    response = requests.get(URL, headers=headers)

    if(response.status_code != 200):
        print_red(f"status code: {response.status_code}")

    ids = []

    response_json = response.json()
    data = response_json['data']

    for item in data:
        print_green(item['id'])


    # with open(TEMP_OUTPUT, 'w', encoding='utf-8') as file:
    #     file.write(response.text)

def read_json(path:str):
    

# get_Bible()

