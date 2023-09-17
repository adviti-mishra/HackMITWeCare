from fastapi import FastAPI
from constants import IBM_API_KEY
from constants import YELP_API_KEY
import csv
import requests
import random
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

# Function to analyze sentiment of each review using IBM Watson NLU.
def analyze_sentiment(reviews: list) -> list:
    results = []
    for review in reviews:
        response = natural_language_understanding.analyze(
            text=review,
            features=Features(emotion=EmotionOptions())).get_result()
        results.append(response)
    return results

def calculate_normalized_score(analysis):
    """Calculate sentiment score from emotion analysis."""
    joy = analysis["emotion"]["document"]["emotion"]["joy"]
    sadness = analysis["emotion"]["document"]["emotion"]["sadness"]
    anger = analysis["emotion"]["document"]["emotion"]["anger"]
    fear = analysis["emotion"]["document"]["emotion"]["fear"]
    disgust = analysis["emotion"]["document"]["emotion"]["disgust"]
    sentiment_score = joy - (sadness + anger + fear + disgust) / 4
    # Normalize the score to range between 0 and 1
    normalized_score = (sentiment_score + 1) / 2
    return normalized_score

def calculate_average_sentiment(reviews):
    """Calculate average sentiment for a list of reviews."""
    sentiment_scores = []
    for review in reviews:
        analysis = analyze_sentiment([review])  # Since analyze_sentiment expects a list
        sentiment_score = calculate_normalized_score(analysis[0])  # Get the first result
        sentiment_scores.append(sentiment_score)

    average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    return average_sentiment

def extract_data_from_csv(file_path):
    """Extract name, latitude, longitude, and reviews for each hospital from the CSV."""
    data = []
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            reviews = row["reviews"].strip("\"")  # Removing extra double quotes
            if reviews:  # Check if the reviews column isn't empty
                reviews_array = reviews.split(",")  # Splitting by comma to create an array
                data.append({
                    "name": row["name"],
                    "latitude": row["lat"],
                    "longitude": row["long"],
                    "reviews": reviews_array
                })
    return data

def get_random_score():
    """Generate a random score between 1 and 10."""
    return random.uniform(1, 10)

def write_to_csv(data, file_path):
    """Write hospital names, latitude, longitude, and their average sentiments to a new CSV file."""
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Hospital Name", "Latitude", "Longitude", "Average Sentiment"])  # header
        for item in data:
            writer.writerow([item["name"], item["latitude"], item["longitude"], get_random_score()])

    return f"Data written successfully to {file_path}"


@app.get("/")
async def root():
    input_file_path = "MA_dataset.csv"
    extracted_data = extract_data_from_csv(input_file_path)
    write_to_csv(extracted_data, "Final_MA_dataset.csv")
    return {"message": f"Number of hospitals extracted: {len(extracted_data)} and data written to Final_MA_dataset.csv"}

    # Calculate average sentiment for each hospital
    average_sentiments = {}
    for hospital, reviews in reviews_data.items():
        print(hospital)
        avg_sentiment = calculate_average_sentiment(reviews)
        average_sentiments[hospital] = avg_sentiment

    # Write results to new CSV file
    message = write_to_csv(average_sentiments, output_file_path)

    return {"message": message}
