from playwright.sync_api import sync_playwright
import json
import pandas as pd
from bs4 import BeautifulSoup
import phonenumbers
from phonenumbers import geocoder, timezone


def get_search_results(search_terms, location, max_pages=1):
    all_content = ""
    for page_num in range(1, max_pages + 1):
        url = f"https://www.yellowpages.com/search?search_terms={search_terms}&geo_location_terms={location}&page={page_num}"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            # Wait for the page to load completely
            page.wait_for_load_state("networkidle")

            # Get the page content
            content = page.content()
            all_content += content + "\n\n"  # Append content from each page

            browser.close()

    return all_content


def parse_and_save_data(html_content, output_file="business_data.csv"):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")
    script_tags = soup.find_all("script", type="application/ld+json")

    # Initialize a list to store the extracted data
    data = []

    # Extract and parse the JSON data
    for script in script_tags:
        try:
            json_data = json.loads(script.string)
        except json.JSONDecodeError:
            # Skip invalid JSON
            continue

        # Handle both single JSON objects and lists
        if isinstance(json_data, list):
            for item in json_data:
                item_type = item.get("@type")
                name = item.get("name")
                address = item.get("address", {}).get("streetAddress")
                rating = item.get("aggregateRating", {}).get("ratingValue")
                review_count = item.get("aggregateRating", {}).get("reviewCount")
                telephone = item.get("telephone")
                opening_hours = item.get("openingHours")

                # Extract phone number details using phonenumbers
                phone_details = {}
                if telephone:
                    try:
                        parsed_number = phonenumbers.parse(
                            telephone, "US"
                        )  # Assume US numbers
                        phone_details["Country"] = geocoder.description_for_number(
                            parsed_number, "en"
                        )
                        phone_details["Timezone"] = timezone.time_zones_for_number(
                            parsed_number
                        )
                        phone_details["Valid"] = phonenumbers.is_valid_number(
                            parsed_number
                        )
                    except phonenumbers.NumberParseException:
                        phone_details = {
                            "Country": "Unknown",
                            "Timezone": "Unknown",
                            "Valid": False,
                        }

                # Append the extracted data to the list
                data.append(
                    {
                        "Type": item_type,
                        "Name": name,
                        "Address": address,
                        "Rating": rating,
                        "Review Count": review_count,
                        "Telephone": telephone,
                        "Opening Hours": opening_hours,
                        "Country": phone_details.get("Country", "Unknown"),
                        "Timezone": phone_details.get("Timezone", "Unknown"),
                        "Valid": phone_details.get("Valid", False),
                    }
                )
        else:
            item_type = json_data.get("@type")
            name = json_data.get("name")
            address = json_data.get("address", {}).get("streetAddress")
            rating = json_data.get("aggregateRating", {}).get("ratingValue")
            review_count = json_data.get("aggregateRating", {}).get("reviewCount")
            telephone = json_data.get("telephone")
            opening_hours = json_data.get("openingHours")

            # Extract phone number details using phonenumbers
            phone_details = {}
            if telephone:
                try:
                    parsed_number = phonenumbers.parse(
                        telephone, "US"
                    )  # Assume US numbers
                    phone_details["Country"] = geocoder.description_for_number(
                        parsed_number, "en"
                    )
                    phone_details["Timezone"] = timezone.time_zones_for_number(
                        parsed_number
                    )
                    phone_details["Valid"] = phonenumbers.is_valid_number(parsed_number)
                except phonenumbers.NumberParseException:
                    phone_details = {
                        "Country": "Unknown",
                        "Timezone": "Unknown",
                        "Valid": False,
                    }

            # Append the extracted data to the list
            data.append(
                {
                    "Type": item_type,
                    "Name": name,
                    "Address": address,
                    "Rating": rating,
                    "Review Count": review_count,
                    "Telephone": telephone,
                    "Opening Hours": opening_hours,
                    "Country": phone_details.get("Country", "Unknown"),
                    "Timezone": phone_details.get("Timezone", "Unknown"),
                    "Valid": phone_details.get("Valid", False),
                }
            )

    # Create a pandas DataFrame from the extracted data
    df = pd.DataFrame(data)

    # Filter out rows where the Type is BreadcrumbList or Place
    df = df[~df["Type"].isin(["BreadcrumbList", "Place"])]

    # Save the filtered DataFrame to a CSV file
    df.to_csv(output_file, index=False)

    print(f"Data has been saved to '{output_file}'")


# Example usage
search_terms = "AI"
location = "San+Francisco%2C+CA"
max_pages = 1  # Number of pages to scrape

# Get the search results
html_content = get_search_results(search_terms, location, max_pages)

# Parse the HTML content and save the data to a CSV file
parse_and_save_data(html_content)
