import configparser
import os

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