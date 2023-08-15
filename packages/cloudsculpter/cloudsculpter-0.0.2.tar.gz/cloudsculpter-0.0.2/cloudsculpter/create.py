import re
import openai
import yaml
import os
import configparser
from cloudsculpter.logger import log
from cloudsculpter.utils import openai_request



def validate_file_name(file_name):
    return bool(re.match('^[a-zA-Z0-9-_]+$', file_name))

def create_template():
    file_name = input("Please provide a name for the template file (use upper or lowercase letters, numbers, - or _): ").strip()
    if not validate_file_name(file_name):
        print("Invalid file name. Please use only upper or lowercase letters, numbers, - or _.")
        return
    
    # Add .yaml extension
    file_name += '.yaml'

    if os.path.exists(file_name):
        log.error(f"File {file_name} already exists.")
        return
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'templates' not in config:
        config['templates'] = {}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("Configuration updated successfully.")

    # Ask for the resources description
    resources_description = input("Please describe the resources you're looking to generate: ").strip()

    # Call OpenAI to provide the list of parameters and resources
    system_message = f"You are a busy and terse DevOps engineer. Create a CloudFormation template with the resources described, including parameters and dependencies you anticipate. Your response should only include the relevant YAML code. The template should be valid and deployable with the stack name {file_name}."
    
    # Prompt for OpenAI
    prompt = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': resources_description}
    ]
    
    # Making the OpenAI request
    cf_template_content = openai_request(prompt)

    # Assume the content is in a YAML-compatible format; additional processing might be required
    with open(file_name, 'w') as file:
        file.write(cf_template_content)
    
    template_path = os.path.abspath(file_name)
    config['templates'][file_name] = template_path

    print(f"File {file_name} has been created successfully.")
    return template_path