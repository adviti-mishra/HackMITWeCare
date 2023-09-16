from fastapi import FastAPI
from constants import IBM_API_KEY
from constants import YELP_API_KEY
import csv
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


@app.get("/")
async def root():
    return "Hello, world!";
