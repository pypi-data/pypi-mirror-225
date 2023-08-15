import os
import yaml
from cloudsculpter.logger import log


def edit_resource(template_content):
    # Ask the user for the resource name
    resource_name = input("Please provide the name of the resource you want to add or edit: ").strip()
    
    # Ask the user to input the YAML code for the resource
    resource_yaml = input("Please provide the YAML code for the resource (you can copy and paste multiple lines): ")
    
    # Load the provided YAML code
    try:
        resource_content = yaml.safe_load(resource_yaml)
    except yaml.YAMLError as e:
        print("Error in the provided YAML code:", e)
        return False

    # Update the resources section with the new or modified resource
    template_content['Resources'][resource_name] = resource_content
    return True

def edit_template():
    file_name = input("Please provide the name of the template you want to edit: ").strip()
    if not file_name.endswith('.yaml'):
        file_name += '.yaml'

    if not os.path.exists(file_name):
        print(f"File {file_name} does not exist.")
        return

    config = configparser.ConfigParser()
    config.read('config.ini')
    
    if 'templates' not in config:
        config['templates'] = {}
    
    config['templates'][template_file_name] = template_path

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
    print("Template created successfully.")

    # Read the existing YAML content
    with open(file_name, 'r') as file:
        template_content = yaml.safe_load(file)

    # Print the current content and ask for modifications
    print(f"Current content of {file_name}:")
    print(yaml.dump(template_content, default_flow_style=False))

    # Edit the template based on user input
    if edit_resource(template_content):
        # Write the updated YAML content back to the file
        with open(file_name, 'w') as file:
            yaml.dump(template_content, file, default_flow_style=False)

        print(f"File {file_name} has been updated successfully.")
    else:
        print("Failed to edit the template.")