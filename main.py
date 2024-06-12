from fastapi import FastAPI, Response
from starlette.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests
import asyncio
import csv
import os
from datetime import datetime


origins = [
    "http://localhost",  
    "http://localhost:3000", 
]


# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to store price data
DATA_DIR = "price_data"

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Function to scrape headphone prices
def scrape_headphone_prices():
    url = "https://www.boat-lifestyle.com/collections/bluetooth-wireless-headphones"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        price_element = soup.find("span", class_="price--highlight")
        if price_element:
            price = price_element["data-price"]
            actual_price = price.removesuffix("00")
            return actual_price
    return None

# Function to store price data in a CSV file
def store_prices_in_csv(price):
    file_path = os.path.join(DATA_DIR, "price_data.csv")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, price])

# Function to fetch the latest price from CSV
def get_latest_price_from_csv():
    file_path = os.path.join(DATA_DIR, "price_data.csv")
    try:
        with open(file_path, mode='r') as file:
            return file.read()
    except FileNotFoundError:
        return None

# Endpoint to fetch latest price
@app.get("/get_latest_price")
async def get_latest_price():
    # Scrape the latest price
    price = scrape_headphone_prices()
    if price:
        # Store the latest price in the CSV file
        store_prices_in_csv(price)
        return {"timestamp": datetime.now(), "price": price}
    else:
        return {"message": "Failed to get latest price"}

# Endpoint to export price data as CSV
@app.get("/export_prices_csv")
async def export_prices_csv():
    file_path = os.path.join(DATA_DIR, "price_data.csv")
    try:
        with open(file_path, mode='r') as file:
            csv_content = file.read()
            return Response(content=csv_content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=price_data.csv"})
    except FileNotFoundError:
        return {"message": "Price data file not found"}


