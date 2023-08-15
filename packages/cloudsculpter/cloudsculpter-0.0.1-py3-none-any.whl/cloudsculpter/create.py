import re
import openai
import yaml
from cloudsculpter.logger import log


def validate_file_name(file_name):
    return bool(re.match('^[a-zA-Z0-9-_]+$', file_name))

def create_template():
    file_name = input("Please provide a name for the template file (use upper or lowercase letters, numbers, - or _): ").strip()
    if not validate_file_name(file_name):
        print("Invalid file name. Please use only upper or lowercase letters, numbers, - or _.")
        return

    config = configparser.ConfigParser()
    config.read('config.ini')
    
    if 'templates' not in config:
        config['templates'] = {}
    
    config['templates'][template_file_name] = template_path

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("Configuration updated successfully.")
        
    # Add .yaml extension
    file_name += '.yaml'

    # Ask for the resources description
    resources_description = input("Please describe the resources you're looking to generate: ").strip()

    # Call OpenAI to provide the list of parameters and resources
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "I need to create a CloudFormation template with the following resources:"},
            {"role": "user", "content": resources_description}
        ]
    )

    # Retrieve the completion and use it as the content of the CloudFormation template
    cf_template_content = response.choices[0].message['content']

    # Assume the content is in a YAML-compatible format; additional processing might be required
    with open(file_name, 'w') as file:
        file.write(cf_template_content)
    
    print(f"File {file_name} has been created successfully.")