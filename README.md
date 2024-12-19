# README

## Overview

This project scrapes business data from Yellow Pages and saves it to a CSV file. It uses Playwright for web scraping, BeautifulSoup for parsing HTML, and pandas for data manipulation and storage.

## Requirements

- Python 3.6+
- Playwright
- BeautifulSoup
- pandas
- phonenumbers

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required Python packages:
    ```sh
    pip install pytest-playwright beautifulsoup4 pandas phonenumbers
    ```

3. Install Playwright browsers:
    ```sh
    playwright install
    ```

## Usage

1. Open the 

fullthing.py

 file and modify the 

search_terms

, 

location

, and 

max_pages

 variables as needed:
    ```python
    search_terms = "AI+Consultants"
    location = "San+Francisco%2C+CA"
    max_pages = 1  # Number of pages to scrape
    ```

2. Run the script:
    ```sh
    python fullthing.py
    ```

3. The scraped data will be saved to 

business_data.csv

 in the project directory.

## Example

To scrape restaurant data from San Francisco, CA, and save it to a CSV file:

1. Set the search terms and location:
    ```python
    search_terms = "AI+Consultants"
    location = "San+Francisco%2C+CA"
    max_pages = 1
    ```

2. Run the script:
    ```sh
    python fullthing.py
    ```

3. The data will be saved to 

business_data.csv

.

## Notes

- The script assumes US phone numbers for parsing and validation.
- The script filters out rows where the type is `BreadcrumbList` or `Place` before saving to the CSV file.

## License

This project is licensed under the MIT License. See the LICENSE file for details.