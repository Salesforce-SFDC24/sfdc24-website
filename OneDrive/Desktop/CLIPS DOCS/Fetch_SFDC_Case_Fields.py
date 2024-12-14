from simple_salesforce import Salesforce

# Replace with your sandbox credentials
USERNAME = "abdus@sfdc24.com.fulldev1"
PASSWORD = "Tflower2020!"
SECURITY_TOKEN = "GLPia7LiQv8r1Y263roXaJ5bN"

# Sandbox login URL
SANDBOX_DOMAIN = "htv--fulldev1.sandbox.my.salesforce.com"


# Connect to Salesforce sandbox
sf = Salesforce(username=USERNAME, password=PASSWORD, security_token=SECURITY_TOKEN, domain="test")

# Fetch Case object metadata
case_metadata = sf.Case.describe()

# Extract field information
print("Fields in Case Object:")
for field in case_metadata["fields"]:
    print(f"{field['name']} ({field['type']}): {field['label']}")
