from simple_salesforce import Salesforce

# Replace with your sandbox credentials
USERNAME = "abdus@sfdc24.com.fulldev1"
PASSWORD = "Tflower2020!"
SECURITY_TOKEN = "GLPia7LiQv8r1Y263roXaJ5bN"

# Sandbox login URL
SANDBOX_DOMAIN = "htv--fulldev1.sandbox.my.salesforce.com"

def test_salesforce_api():
    """Log into Salesforce sandbox and fetch one account record."""
    try:
        # Connect to Salesforce
        sf = Salesforce(
            username=USERNAME,
            password=PASSWORD,
            security_token=SECURITY_TOKEN,
            domain='test'
        )
        print("Connected to Salesforce successfully!")

        # Fetch one Account record
        accounts = sf.query("SELECT Id, Name FROM Account LIMIT 1")
        if accounts["records"]:
            print("Fetched one Account record:")
            print(f"ID: {accounts['records'][0]['Id']}")
            print(f"Name: {accounts['records'][0]['Name']}")
        else:
            print("No Account records found.")
    except Exception as e:
        print(f"Error connecting to Salesforce or fetching records: {e}")

if __name__ == "__main__":
    test_salesforce_api()
