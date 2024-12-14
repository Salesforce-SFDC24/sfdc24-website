import subprocess

def run_sfdx_command(command):
    """Run a Salesforce CLI command and return the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"Command succeeded: {command}")
            return result.stdout
        else:
            print(f"Command failed: {command}")
            print(result.stderr)
            return None
    except Exception as e:
        print(f"Error running command: {e}")
        return None

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
    response = run_sfdx_command(command)
    if response:
        print(f"Field {field_name} created successfully!")
    else:
        print(f"Failed to create field {field_name}.")

if __name__ == "__main__":
    ALIAS = "fulldev1"
    BIG_OBJECT_API_NAME = "Case_Archive__b"

    # Missing fields from the first script
    missing_fields = [
        {"name": "Custom_Field__c", "type": "Text", "label": "Custom Field"}
    ]

    # Create fields in the Big Object
    for field in missing_fields:
        create_big_object_field(
            alias=ALIAS,
            big_object_api_name=BIG_OBJECT_API_NAME,
            field_name=field["name"],
            field_type=field["type"],
            field_label=field["label"]
        )
