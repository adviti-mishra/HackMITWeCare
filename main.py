from fastapi import FastAPI
from constants import ibm_api_key
import csv
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(ibm_api_key)
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


reviews_list = read_csv('dummy_data.csv')


# Analyze the reviews and return the emotion analysis from IBM Watson NLU
@app.get("/")
async def root():
    # Just taking the first review for the sake of example
    sample_review = reviews_list[0]
    response = natural_language_understanding.analyze(
        text=sample_review,
        features=Features(emotion=EmotionOptions())).get_result()

    return {"emotion_analysis": response}
