from bs4 import BeautifulSoup
import requests
import json
from jsonpath_ng import parse
import jsonpath_ng

# Load the table from a JSON file
with open('data.json', 'r') as json_file:
  table = json.load(json_file)

# Define the column containing the product page links
link_col = 'Link'

# Define the JSONPath expressions
price_expr = jsonpath_ng.parse("$..price")
currency_expr = jsonpath_ng.parse("$..priceCurrency")
# price_expr = parse("$...price")

def value(a):
  return a.value


# Define the scraping function
def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = {}

    # Extract additional data from JSON-LD
    script_tag = soup.find('script', type='application/ld+json')
    if script_tag:
        # Extract the JSON-LD script content
        script_content = script_tag.string

        # Parse the JSON content
        json_id = json.loads(script_content)

        # Use JSONPath to extract the price value
        # descendants = Descendants(data, price_expr)
        if price_expr:
            for match in price_expr.find(json_id):
               data['Price'] = match.value
        if currency_expr:
            for match in currency_expr.find(json_id):
               data['Currency'] = match.value

    # Extract additional data from HTML
    price_element = soup.find('span', class_='price')
    if price_element:
        data['Price'] = price_element.text.strip()

    return data

# Iterate over each row in the table
for row in table:
    # Check if the price is missing
    if not hasattr(row, 'Price') or row['Price'] == '':
        # Scrape the product page to get the missing data
        data = scrape_data(row[link_col])

        # Update the table with the extracted data
        for key, value in data.items():
            row[key] = value

    # Print the in-progress table
    print(row)
    # save the in-progress table to a JSON file
    with open('result.json', 'w') as json_file:
      json.dump(table, json_file, indent=2)

# Print the updated table
for row in table:
    print(row)

