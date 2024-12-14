import subprocess
import json

def run_sfdx_command(command):
    """Run a Salesforce CLI command and return JSON output."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"Command failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error running command: {e}")
        return None

def get_sobject_fields(sobject_name, alias):
    """Get all fields from a Salesforce object."""
    print(f"Fetching fields for {sobject_name}...")
    command = f"sfdx force:schema:sobject:describe -s {sobject_name} -u {alias} --json"
    response = run_sfdx_command(command)
    if response and "result" in response:
        fields = response["result"]["fields"]
        return {field["name"]: field["type"] for field in fields}
    else:
        print(f"Failed to fetch fields for {sobject_name}.")
        return {}

def compare_fields(case_fields, archive_fields):
    """Compare Case fields with Big Object fields."""
    missing_fields = []
    for field, field_type in case_fields.items():
        if field not in archive_fields:
            missing_fields.append((field, field_type))
    return missing_fields

if __name__ == "__main__":
    CASE_OBJECT = "Case"
    BIG_OBJECT = "Case_Archive__b"
    ALIAS = "fulldev1"

    # Get fields for Case and Case_Archive__b
    case_fields = get_sobject_fields(CASE_OBJECT, ALIAS)
    big_object_fields = get_sobject_fields(BIG_OBJECT, ALIAS)

    # Compare fields and identify missing ones
    missing_fields = compare_fields(case_fields, big_object_fields)
    print("\nMissing Fields:")
    for field, field_type in missing_fields:
        print(f"{field} ({field_type})")
