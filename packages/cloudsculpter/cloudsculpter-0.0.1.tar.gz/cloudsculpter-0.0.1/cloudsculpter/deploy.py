import os
import boto3
import time
from cloudsculpter.fix import analyze_and_fix
from cloudsculpter.logger import log


def deploy_template():
    client = boto3.client('cloudformation')

    template_name = input("Please provide the name of the template you want to deploy: ").strip()
    if not template_name.endswith('.yaml'):
        template_name += '.yaml'

    if not os.path.exists(template_name):
        print(f"File {template_name} does not exist.")
        return

    # Read the template content
    with open(template_name, 'r') as file:
        template_body = file.read()

    # Ask for the stack name
    stack_name = input("Please provide a name for the CloudFormation stack: ").strip()

    while True:
        # Deploy the template
        try:
            response = client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Capabilities=[
                    'CAPABILITY_IAM',  # Add other capabilities if needed
                ],
            )
            print(f"Stack {stack_name} is being deployed...")

            # Monitor the deployment status
            while True:
                status = client.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
                print(f"Current status: {status}")

                if status == 'CREATE_COMPLETE':
                    print(f"Deployment of stack {stack_name} is complete.")
                    return

                if status in ['ROLLBACK_COMPLETE', 'CREATE_FAILED']:
                    break

                time.sleep(5)  # Polling interval

        except Exception as e:
            print(f"Failed to deploy the stack {stack_name}. Error: {e}")

        # Analyze and fix the failure
        approve_fix, suggested_fix = analyze_and_fix(stack_name)
        if approve_fix:
            # Modify the template based on the suggested fix
            # This may require parsing and editing the YAML content
            # Example: template_body = apply_suggested_fix(template_body, suggested_fix)
            pass
        else:
            print(f"Deployment of stack {stack_name} failed.")
            return