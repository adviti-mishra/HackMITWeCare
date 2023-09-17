

# import json
# from ibm_watson import NaturalLanguageUnderstandingV1
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from ibm_watson.natural_language_understanding_v1 \
#     import Features, EmotionOptions
#
# authenticator = IAMAuthenticator('_J9W5CsDJjWzzY554OSj_uoL7iAnpqEUZc52nVDAEFVm')
# natural_language_understanding = NaturalLanguageUnderstandingV1(
#     version='2022-04-07',
#     authenticator=authenticator
# )
#
# natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/d6ed091b-fd84-4d35-ba4d-74f01385aedc')
#
# response = natural_language_understanding.analyze(
#     html="<html><head><title>Fruits</title></head><body><h1>Apples and Oranges</h1><p>I really really hate apples! I don't like oranges.</p></body></html>",
#     features=Features(emotion=EmotionOptions(targets=['I really really hate apples!', 'oranges']))).get_result()
#
# print(json.dumps(response, indent=2))









from serpapi import GoogleSearch

import csv

import requests

api_key = "YWCtoJ7vrEt5Wx-uB9yM-OAGZaO8k4oXnOdw-PfZabRuj2qDGj-F_k4TnEFO2pWLoAcNIjGp53UVUcdQNItlwxMNhsvZMQNhXo9xr4NfA6L4UgjP0sgegPMys1QGZXYx"




#### GET ID GIVEN NAME:

STATE = "MA"

url = f"https://api.yelp.com/v3/businesses/search?location={STATE}&term=hospital&categories=&sort_by=best_match&limit=50"

headers = {
    "accept": "application/json",
    "Authorization": F"Bearer {api_key}"
}

response1 = requests.get(url, headers=headers)

print(response1.json())


########################################################################################################################


hospitals = response1.json()['businesses']
for hospital in hospitals:
    # print("Name:", hospital['name'])
    # print("ID:", hospital['id'])

    NAME = hospital['name']
    ID = hospital['id']
    latitude = hospital["coordinates"]["latitude"]
    longitude = hospital["coordinates"]["longitude"]

    params = {
        "engine": "yelp_reviews",
        "place_id": f"{ID}",
        "sortby": "relevance_desc",
        "api_key": "4c9ddfdad7f033b21de032ef7c76141bcbfe64da79c70b696bef3efe3b0e9796"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    print(results)
    REVIEWS = [review['comment']['text'] for review in results['reviews']]

    fields = [NAME, ID, longitude, latitude, REVIEWS]
    with open(r'name2', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)




