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


# Function to get all yelp reviews from a specific bu`siness id and returns a list
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
def calculate_sentiment_from_analysis(analysis):
    """Calculate sentiment score from emotion analysis."""
    joy = analysis["emotion"]["document"]["emotion"]["joy"]
    sadness = analysis["emotion"]["document"]["emotion"]["sadness"]
    sentiment_score = joy - sadness
    # Normalize the score to range between 0 and 1
    normalized_score = (sentiment_score + 1) / 2
    return normalized_score

def extract_reviews_from_csv(file_path):
    """Extract reviews for each hospital from the CSV, safely handling missing keys."""
    reviews_data = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # BUG BELOW
            print(row)
            reviews_data[row["name"]] = row[" reviews"]
            # BUG ABOVE
    return reviews_data

def calculate_average_sentiment(reviews):
    """Calculate average sentiment for a list of reviews."""
    sentiment_scores = []
    for review in reviews:
        analysis = analyze_sentiment([review])  # Since analyze_sentiment expects a list
        sentiment_score = calculate_sentiment_from_analysis(analysis[0])  # Get the first result
        sentiment_scores.append(sentiment_score)

    average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    return average_sentiment


def write_to_csv(data, file_path):
    """Write hospital names and their average sentiments to a new CSV file."""
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Hospital Name", "Average Sentiment"])  # header
        for hospital, sentiment in data.items():
            writer.writerow([hospital, sentiment])

    return f"Data written successfully to {file_path}"


@app.get("/")
async def root():
    input_file_path = "MA_dataset.csv"
    output_file_path = "Final_MA_dataset.csv"

    # Calculate average sentiment for each hospital
    reviews_data = extract_reviews_from_csv(input_file_path)
    print(f"Number of hospitals extracted: {len(reviews_data)}")

    # Calculate average sentiment for each hospital
    average_sentiments = {}
    for hospital, reviews in reviews_data.items():
        print(hospital)
        avg_sentiment = calculate_average_sentiment(reviews)
        average_sentiments[hospital] = avg_sentiment

    # Write results to new CSV file
    message = write_to_csv(average_sentiments, output_file_path)

    return {"message": message}
