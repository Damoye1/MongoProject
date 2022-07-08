import pymongo # this imports the pymongo library
import requests # this imports the requests library
from pprint import pprint # imports pprint

client = pymongo.MongoClient() # connects to mongodb
db = client['starwars'] # accesses the starwars database


def api_collector(link): # pulls all the API information into pycharm
    api_result = requests.request('GET', link).json()['results']
    return api_result


def api_for_every_page(): # This function will put the API docs in a list for each page
    link = "https://swapi.dev/api/starships/?page=1"
    api_list = []
    i = 1
    while requests.request('GET', link).status_code != 404: # will stop looking once the status code is an error 404
        for information in api_collector(link):
            api_list.append(information)
        i += 1
        link = f"https://swapi.dev/api/starships/?page={i}"

    for doc in api_list: # updates all the pilots to objectID's
        for pilot_url in doc['pilots']:
            pilot_names = requests.request('GET', pilot_url).json()['name']
            pilot_id = db.characters.find_one({'name': pilot_names}, {'_id': 1})
            doc['pilots'][doc['pilots'].index(pilot_url)] = pilot_id['_id']

    exec(f'db.starships.drop()') # drops the starships collection if it already exists
    db.create_collection('starships')
    for x in range(len(api_list)):
        db.starships.insert_one(api_list[x])
    return api_list
    # inserts all docs in api list into the starships collection

if __name__ == "__main__": # calls the API for every page function
    pprint(api_for_every_page())