from fastapi import FastAPI
import csv

app = FastAPI()

# Function to read CSV and return list of reviews
def read_csv(filename: str) -> list:
    reviews = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            reviews.append(row['Review'])
    return reviews

reviews_list = read_csv('dummy_data.csv')  # replace 'your_csv_filename.csv' with the actual name of your CSV file

@app.get("/")
async def root():
    return {"reviews": reviews_list}
