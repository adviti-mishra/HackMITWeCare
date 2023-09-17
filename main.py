from fastapi import FastAPI
from constants import IBM_API_KEY
from constants import YELP_API_KEY
import csv
import requests
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(IBM_API_KEY)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
)

service_url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com"
natural_language_understanding.set_service_url(service_url)

app = FastAPI()


# Function to read CSV and return list of reviews
def read_csv(filename: str) -> list:
    reviews = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            reviews.append(row['Review'])
    return reviews


# Function to analyze sentiment of each review using IBM Watson NLU.
def analyze_sentiment(reviews: list) -> list:
    results = []
    for review in reviews:
        response = natural_language_understanding.analyze(
            text=review,
            features=Features(emotion=EmotionOptions())).get_result()
        results.append(response)
    return results


# Function to get all yelp reviews from a specific business id and returns a list
def get_yelp_reviews(business_id: str):
    # API endpoint
    headers = {
        'Authorization': f"Bearer {YELP_API_KEY}",
    }

    url = f"https://api.yelp.com/v3/businesses/{business_id}/reviews?limit=20"

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract the text of the reviews and return
        for row in data["reviews"]:
            print(row["text"])
        return data['reviews']
    else:
        # Print error and return empty list if unsuccessful
        print(f"Error {response.status_code}: {response.text}")
        return []


# Adviti will work on function below
def calculate_review_sentiment(review):
    # Should return a number, 0 < x < 1 that represents individual review sentiment
    print(review)
    return

# We will probably need below function too
def calculate_average_sentiment_for_hopsital(review_sentiment_list):
    # Should return a number, 0 < x < 1 that represents ALL review sentiment for specific hospital
    return

@app.get("/")
async def root():
    reviews = read_csv(filename: str) -> list:
    
