import subprocess
import json
import os

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

def create_big_object_field(alias, big_object_api_name, field_name, field_type, field_label):
    """Create a field in the Big Object."""
    print(f"Creating field {field_name} in Big Object {big_object_api_name}...")
    metadata_file_content = f"""
<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>{big_object_api_name}.{field_name}</fullName>
    <label>{field_label}</label>
    <type>{field_type}</type>
</CustomField>
"""
    # Save metadata to file
    field_file = f"{field_name}.field-meta.xml"
    with open(field_file, "w") as f:
        f.write(metadata_file_content)

    # Deploy metadata using SFDX
    command = f"sfdx force:mdapi:deploy -f {field_file} -u {alias} --wait 10"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Field {field_name} created successfully!")
        os.remove(field_file)  # Clean up the metadata file
    else:
        print(f"Failed to create field {field_name}: {result.stderr}")

if __name__ == "__main__":
    CASE_OBJECT = "Case"
    BIG_OBJECT = "Case_Archive__b"
    ALIAS = "fulldev1"

    # Step 1: Fetch fields for Case and Case_Archive__b
    case_fields = get_sobject_fields(CASE_OBJECT, ALIAS)
    big_object_fields = get_sobject_fields(BIG_OBJECT, ALIAS)

    # Step 2: Compare fields and identify missing ones
    missing_fields = compare_fields(case_fields, big_object_fields)

    print("\nMissing Fields:")
    for field, field_type in missing_fields:
        print(f"{field} ({field_type})")

    # Step 3: Create missing fields in the Big Object
    for field, field_type in missing_fields:
        create_big_object_field(
            alias=ALIAS,
            big_object_api_name=BIG_OBJECT,
            field_name=field,
            field_type="Text" if field_type == "string" else field_type,  # Map to valid metadata types
            field_label=field.replace("_", " ")
        )
