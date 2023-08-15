import argparse
import configparser
from cloudsculpter.create import create_template
from cloudsculpter.edit import edit_template
from cloudsculpter.deploy import deploy_template, set_session_credentials
from cloudsculpter.fix import analyze_and_fix
from cloudsculpter.logger import log

def main():
    parser = argparse.ArgumentParser(description="CloudSculpter - A Python Package for automating CloudFormation Management with LLMs")
    subparsers = parser.add_subparsers(dest="action", help="Choose an action to perform")

    create_parser = subparsers.add_parser('create', help='Create a CloudFormation template')
    edit_parser = subparsers.add_parser('edit', help='Edit an existing CloudFormation template')
    deploy_parser = subparsers.add_parser('deploy', help='Deploy a CloudFormation template')
    fix_parser = subparsers.add_parser('fix', help='Analyze and fix a failed CloudFormation deployment')
    config_parser = subparsers.add_parser('config', help='Configure CloudSculpter')
    config_parser.add_argument('--api-key', required=False, help='OpenAI API key')
    config_parser.add_argument('--profile-name', required=False, help='AWS profile name')
    config_parser.add_argument('--aws-access-key-id', required=False, help='AWS Access Key ID')
    config_parser.add_argument('--aws-secret-access-key', required=False, help='AWS Secret Access Key')
    config_parser.add_argument('--aws-session-token', required=False, help='AWS Session Token')
    config_parser.add_argument('--region', required=False, help='AWS Region')
    config_parser.add_argument('--output', required=False, help='AWS Output Format')

    args = parser.parse_args()

    if args.action in ['create', 'edit', 'deploy', 'fix']:
        if not set_session_credentials():
            log.error("Failed to set AWS session credentials.")
            return

    if args.action == 'create':
        template = create_template()
        if template:
            deploy_template(template)
    elif args.action == 'edit':
        template = edit_template()
        if template:
            deploy_template(template)
    elif args.action == 'deploy':
        deploy_template()
    elif args.action == 'fix':
        analyze_and_fix()
    elif args.action == 'config':
        config = configparser.ConfigParser()
        config.read('config.ini') # Read existing config if available

        if 'aws' not in config:
            config['aws'] = {}

        if args.api_key:
            config['openai'] = {'api_key': args.api_key}
        if args.profile_name:
            config['aws']['profile_name'] = args.profile_name
        if args.aws_access_key_id:
            config['aws']['aws_access_key_id'] = args.aws_access_key_id
        if args.aws_secret_access_key:
            config['aws']['aws_secret_access_key'] = args.aws_secret_access_key
        if args.aws_session_token:
            config['aws']['aws_session_token'] = args.aws_session_token
        if args.region:
            config['aws']['region'] = args.region
        if args.output:
            config['aws']['output'] = args.output
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        log.info("Configuration updated successfully.")
        return
    else:
        parser.print_help()

if __name__ == "__main__":
    main()