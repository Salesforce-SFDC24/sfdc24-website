import shopify


# Set Shopify store credentials
API_KEY = "30aabf6b246ebac32146ed0d94f4ca8c"
PASSWORD = "59a8256e088258dcf718cea48e230806"
SHOP_NAME = "BAR-24-Partner-Dev-Site"  # e.g., "example-store"

# Connect to the store
shop_url = f"https://{API_KEY}:{PASSWORD}@{SHOP_NAME}.myshopify.com/admin/api/2023-01"
shopify.ShopifyResource.set_site(shop_url)

import requests

# Base URL for Shopify API
BASE_URL = f"https://{SHOP_NAME}.myshopify.com/admin/api/2023-01"

def fetch_products():
    """
    Fetch product details including title and price from Shopify.
    """
    url = f"{BASE_URL}/products.json"  # Endpoint for products
    response = requests.get(url, auth=(API_KEY, PASSWORD))

    if response.status_code == 200:
        products = response.json()['products']  # Parse JSON response
        print("Products and Prices:")
        for product in products:
            print(f"Product: {product['title']}")
            for variant in product['variants']:
                print(f" - Variant: {variant['title']}, Price: {variant['price']}")
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    fetch_products()