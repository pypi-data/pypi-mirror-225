import configparser
import os
import openai
import boto3

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def write_config(config):
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def update_api_key(api_key):
    config = read_config()
    config['openai'] = {'api_key': api_key}
    write_config(config)

def set_session_credentials():
    """Set the AWS session credentials based on the configuration file"""
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Check if the 'aws' section is present in the configuration file, and create it if not
    if 'aws' not in config:
        config['aws'] = {}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        log.info("AWS section created in config.ini. Please run 'cloudsculpter config' to configure your AWS credentials.")
        return False

    # Check for profile name first
    profile_name = config['aws'].get('profile_name', None)
    if profile_name:
        region = config['aws'].get('region', None)
        boto3.setup_default_session(profile_name=profile_name, region_name=region)
        return True

    # Check for hardcoded credentials
    aws_access_key_id = config['aws'].get('aws_access_key_id', None)
    aws_secret_access_key = config['aws'].get('aws_secret_access_key', None)
    aws_session_token = config['aws'].get('aws_session_token', None)
    region = config['aws'].get('region', None)

    if aws_access_key_id and aws_secret_access_key and aws_session_token:
        boto3.setup_default_session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region
        )
        return True

    # Ask user for named profile or access key credentials (existing code)

    # Save the updated configuration to file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    # Call the function recursively to set up the session with the new credentials
    return set_session_credentials()

def add_template_path(template_name, template_path):
    config = read_config()
    
    if 'templates' not in config:
        config['templates'] = {}
    
    config['templates'][template_name] = os.path.abspath(template_path)
    write_config(config)

def get_api_key():
    config = read_config()
    return config['openai']['api_key']

def get_template_paths():
    config = read_config()
    return dict(config['templates']) if 'templates' in config else {}

def openai_request(prompt):
    """
    Makes a request to OpenAI's GPT-4 model with the given prompt.
    
    :param prompt: The prompt for the OpenAI model (messages dictionary)
    :return: The response content from the OpenAI model, excluding lines that start with triple backticks
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=prompt
    )
    content = response.choices[0].message['content']
    
    # Exclude lines that start with triple backticks
    content = '\n'.join([line for line in content.splitlines() if not line.startswith('```')])
    
    return content