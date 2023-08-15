import argparse
from cloudsculpter.create import create_template
from cloudsculpter.edit import edit_template
from cloudsculpter.deploy import deploy_template
from cloudsculpter.fix import analyze_and_fix
from cloudsculpter.logger import log

def main():
    parser = argparse.ArgumentParser(description="DevOps Guru Python Package for CloudFormation Management")
    subparsers = parser.add_subparsers(dest="action", help="Choose an action to perform")

    create_parser = subparsers.add_parser('create', help='Create a CloudFormation template')
    edit_parser = subparsers.add_parser('edit', help='Edit an existing CloudFormation template')
    deploy_parser = subparsers.add_parser('deploy', help='Deploy a CloudFormation template')
    fix_parser = subparsers.add_parser('fix', help='Analyze and fix a failed CloudFormation deployment')
    config_parser = subparsers.add_parser('config', help='Configure the OpenAI API key')
    config_parser.add_argument('--api-key', required=True, help='OpenAI API key')

    args = parser.parse_args()

    if args.action == 'create':
        create_template()
    elif args.action == 'edit':
        edit_template()
    elif args.action == 'deploy':
        deploy_template()
    elif args.action == 'fix':
        analyze_and_suggest_fixes()
    elif args.action == 'config':
        config = configparser.ConfigParser()
        config.read('config.ini') # Read existing config if available
        if args.api_key:
            config['openai'] = {'api_key': args.api_key}

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print("Configuration updated successfully.")
        return
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
