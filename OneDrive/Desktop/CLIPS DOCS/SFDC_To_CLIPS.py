from simple_salesforce import Salesforce
from clips import Environment

# Connect to Salesforce
sf = Salesforce(
    username='abdus@sfdc24.com.fulldev1',
    password='Tflower2020!',
    security_token='your-security-token',
    domain='test'
)

def fetch_opportunities():
    """
    Fetch Opportunities from Salesforce.
    """
    query = """
    SELECT Id, Name, Amount, Probability
    FROM Opportunity
    WHERE IsClosed = False
    """
    opportunities = sf.query(query)
    return opportunities['records']

def evaluate_opportunities_with_clips(data):
    """
    Load Salesforce data into CLIPS and evaluate rules.
    """
    # Initialize CLIPS environment
    env = Environment()

    # Load rules
    env.load("rules.clp")

    # Insert data into CLIPS
    for record in data:
        opportunity_fact = f"""
        (opportunity
            (id "{record['Id']}")
            (name "{record['Name']}")
            (value {int(record['Amount'] or 0)})
            (risk {int(record['Probability'] or 0)})
        )
        """
        env.assert_string(opportunity_fact)

    # Run rules
    print("Running CLIPS...")
    env.run()

if __name__ == "__main__":
    # Fetch data from Salesforce
    data = fetch_opportunities()
    
    # Evaluate data with CLIPS
    evaluate_opportunities_with_clips(data)
