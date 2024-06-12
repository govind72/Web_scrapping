# Web Scraping Project

This project is a web scraping application built with FastAPI. It scrapes headphone prices from a specified website and provides endpoints to fetch the latest price and export price history as a CSV file.

## Requirements

- Python 3.7+
- FastAPI
- BeautifulSoup4
- Requests

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/web_scraping.git
   cd web_scraping
   ```
2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

3. Start the FastAPI development server:
   ```sh
   uvicorn main:app --reload
