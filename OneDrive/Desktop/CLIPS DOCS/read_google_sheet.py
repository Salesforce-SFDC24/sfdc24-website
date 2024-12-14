import gspread
from google.oauth2.service_account import Credentials

# Path to your service account JSON file
CREDENTIALS_FILE = "service-account.json"

# URL or ID of the Google Sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/1zXV3s7y43jc1Y67f7532mZRi_bpXOjmeuVHnzxDUIuU/edit?usp=sharing"

# Define the scope for Google Sheets API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def read_google_sheet(sheet_url):
    """Reads all data from a Google Sheet."""
    # Authenticate with Google Sheets API
    credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.sheet1  # Access the first worksheet

    # Fetch all data
    data = worksheet.get_all_records()  # Returns a list of dictionaries
    return data

if __name__ == "__main__":
    # Read the Google Sheet
    data = read_google_sheet(SHEET_URL)

    # Print the data
    print("Google Sheet Data:")
    for row in data:
        print(row)
