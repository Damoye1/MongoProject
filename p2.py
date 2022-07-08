import pymongo
import requests
from pprint import pprint

client = pymongo.MongoClient()
db = client['starwars']


def api_collector(link):
    api_result = requests.request('GET', link).json()['results']
    return api_result


def api_for_every_page():
    link = "https://swapi.dev/api/starships/?page=1"
    api_list = []
    i = 1
    while requests.request('GET', link).status_code != 404:
        for information in api_collector(link):
            api_list.append(information)
        i += 1
        link = f"https://swapi.dev/api/starships/?page={i}"

    for doc in api_list:
        for pilot_url in doc['pilots']:
            pilot_names = requests.request('GET', pilot_url).json()['name']
            pilot_id = db.characters.find_one({'name': pilot_names}, {'_id': 1})
            doc['pilots'][doc['pilots'].index(pilot_url)] = pilot_id['_id']

    exec(f'db.starships.drop()')
    db.create_collection('starships')
    for x in range(len(api_list)):
        db.starships.insert_one(api_list[x])
    return api_list


if __name__ == "__main__":
    pprint(api_for_every_page())
