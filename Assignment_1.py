import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize empty lists to store the data
product_urls = []
product_names = []
product_prices = []
ratings = []
reviews = []

# Specify the number of pages you want to scrape
num_pages = 20

# Loop through each page
for page in range(1, num_pages + 1):
    url = f'https://www.amazon.in/s?k=bags&page={page}'

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all product containers
        products = soup.find_all('div', {'data-component-type': 's-search-result'})

        # Extract data for each product
        for product in products:
            # Product URL
            product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
            product_urls.append(product_url)

            # Product Name
            product_name = product.find('span', {'class': 'a-text-normal'}).text
            product_names.append(product_name)

            # Product Price
            product_price_element = product.find('span', {'class': 'a-price-whole'})
            product_price = product_price_element.text if product_price_element else 'N/A'
            product_prices.append(product_price)

            # Rating
            rating = product.find('span', {'class': 'a-icon-alt'})
            ratings.append(rating.text if rating else 'N/A')

            # Number of Reviews
            num_reviews = product.find('span', {'class': 'a-size-base'})
            reviews.append(num_reviews.text if num_reviews else 'N/A')

# Create a DataFrame to store the data
data = {
    'Product URL': product_urls,
    'Product Name': product_names,
    'Product Price': product_prices,
    'Rating': ratings,
    'Number of Reviews': reviews
}

df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv('amazon_products.csv', index=False)

print(f'Scraped data from {num_pages} pages and saved to amazon_products.csv')
