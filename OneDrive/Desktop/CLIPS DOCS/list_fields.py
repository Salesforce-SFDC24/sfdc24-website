import subprocess
import json

def run_sfdx_command(command):
    """Run a Salesforce CLI command and return the JSON output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"Command failed: {command}")
            print(result.stderr)
            return None
    except Exception as e:
        print(f"Error running command: {e}")
        return None

def list_case_fields(alias):
    """List fields from the Case object."""
    print("Fetching Case object fields...")
    command = f"sfdx force:schema:sobject:describe -s Case -u {alias} --json"
    response = run_sfdx_command(command)
    if response:
        fields = response['result']['fields']
        print(f"Found {len(fields)} fields in the Case object:")
        for field in fields:
            print(f"{field['name']} ({field['type']}): {field['label']}")
        return fields
    else:
        print("Failed to fetch Case object fields.")
        return []

def list_big_object_fields(alias, big_object_api_name):
    """List fields from the Big Object."""
    print(f"Fetching fields from Big Object {big_object_api_name}...")
    command = f"sfdx force:schema:sobject:describe -s {big_object_api_name} -u {alias} --json"
    response = run_sfdx_command(command)
    if response:
        fields = response['result']['fields']
        print(f"Found {len(fields)} fields in the Big Object:")
        for field in fields:
            print(f"{field['name']} ({field['type']}): {field['label']}")
        return fields
    else:
        print("Failed to fetch Big Object fields.")
        return []

if __name__ == "__main__":
    ALIAS = "fulldev1"
    BIG_OBJECT_API_NAME = "Case_Archive__b"

    # Fetch fields from Case object
    case_fields = list_case_fields(ALIAS)

    # Fetch fields from Big Object
    big_object_fields = list_big_object_fields(ALIAS, BIG_OBJECT_API_NAME)

    # List missing fields
    if case_fields and big_object_fields:
        big_object_field_names = {field['name'] for field in big_object_fields}
        missing_fields = [
            field for field in case_fields if field['name'] not in big_object_field_names
        ]
        print(f"\nMissing fields in {BIG_OBJECT_API_NAME}:")
        for field in missing_fields:
            print(f"{field['name']} ({field['type']}): {field['label']}")
