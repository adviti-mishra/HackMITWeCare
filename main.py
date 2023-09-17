from fastapi import FastAPI
from constants import IBM_API_KEY
from constants import YELP_API_KEY
import csv
import requests
import random
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from transformers import BartForConditionalGeneration, BartTokenizer

authenticator = IAMAuthenticator(IBM_API_KEY)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
)

service_url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com"
natural_language_understanding.set_service_url(service_url)

app = FastAPI()

# Function to analyze sentiment of each review using IBM Watson NLU.
def analyze_sentiment(review: str) -> dict:
    if len(review) > 20:  # Assuming a minimum length for meaningful analysis
        print(f"Scoring reviews: {review}")  # Printing the review being scored
        response = natural_language_understanding.analyze(
            text=review,
            features=Features(emotion=EmotionOptions())).get_result()
        return response
    else:
        print(f"Review too short for scoring: {review}")
        return None


def calculate_normalized_score(analysis):
    """Calculate sentiment score from emotion analysis."""
    emotions = analysis["emotion"]["document"]["emotion"]
    joy = emotions["joy"]
    sadness = emotions["sadness"]
    anger = emotions["anger"]
    fear = emotions["fear"]
    disgust = emotions["disgust"]
    sentiment_score = joy - (sadness + anger + fear + disgust) / 4
    # Normalize the score to range between 0 and 1
    normalized_score = (sentiment_score + 1) / 2
    return normalized_score


def calculate_average_sentiment(reviews):
    """Calculate average sentiment and emotion scores for a list of reviews."""
    sentiment_scores = []
    emotion_totals = {"joy": 0, "sadness": 0, "anger": 0, "fear": 0, "disgust": 0}

    for review in reviews:
        analysis = analyze_sentiment(review)  # analyze_sentiment now expects a single review
        if analysis:  # Check if a valid analysis is returned
            sentiment_score = calculate_normalized_score(analysis)
            print(f"Finalized normalized score: {sentiment_score}")
            sentiment_scores.append(sentiment_score)

            for emotion in emotion_totals:
                emotion_totals[emotion] += analysis["emotion"]["document"]["emotion"][emotion]

    # Calculate average sentiment and emotions
    num_reviews = len(sentiment_scores)
    average_sentiment = sum(sentiment_scores) / num_reviews
    average_emotions = {emotion: emotion_totals[emotion] / num_reviews for emotion in emotion_totals}

    return average_sentiment, average_emotions


def extract_data_from_csv(file_path):
    """Extract name, latitude, longitude, and reviews for each hospital from the CSV."""
    data = []
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            reviews = row["reviews"]
            if reviews:  # Check if the reviews column isn't empty
                # Given the structure of your data, the reviews seem to be encapsulated in double quotes
                # and separated by commas within the double quotes. Therefore, we'll handle them as single strings.
                data.append({
                    "name": row["name"],
                    "latitude": row["lat"],
                    "longitude": row["long"],
                    "reviews": [reviews]  # Wrapping it in a list to keep the structure consistent
                })
    return data


def write_to_csv(data, file_path):
    """Write hospital names, latitude, longitude, average sentiments, and average emotion scores to a new CSV file."""
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Hospital Name", "Latitude", "Longitude", "Average Sentiment", "Joy", "Sadness", "Anger", "Fear", "Disgust", "summary"])  # header
        for item in data:
            writer.writerow([item["name"], item["latitude"], item["longitude"], item["score"], item["emotions"]["joy"], item["emotions"]["sadness"], item["emotions"]["anger"], item["emotions"]["fear"], item["emotions"]["disgust"], item["summary"]])

    return f"Data written successfully to {file_path}"

def get_summary(reviews):
    result_string = ''.join(reviews)
    model_name = "facebook/bart-large-cnn"
    model = BartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = BartTokenizer.from_pretrained(model_name)
    inputs = tokenizer.encode("summarize: " + result_string, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

@app.get("/")
async def root():
    input_file_path = "MA_dataset.csv"
    extracted_data = extract_data_from_csv(input_file_path)

    # Calculate average sentiment for each hospital and update the data with the score and emotions
    for item in extracted_data:
        avg_sentiment, avg_emotions = calculate_average_sentiment(item["reviews"])
        item["score"] = avg_sentiment
        item["emotions"] = avg_emotions
        item["summary"] = get_summary(item["reviews"])

    # Write results to new CSV file
    message = write_to_csv(extracted_data, "Final_MA_dataset2.csv")

    return {"message": message}
