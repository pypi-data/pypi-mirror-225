import boto3
import openai
from cloudsculpter.logger import log


def analyze_and_fix(stack_name):
    # Get the events related to the stack failure
    client = boto3.client('cloudformation')
    events = client.describe_stack_events(StackName=stack_name)['StackEvents']

    # Analyze the failure and create a message for OpenAI
    failure_message = "The CloudFormation stack deployment failed. Here are the details:\n"
    for event in events:
        if event['ResourceStatus'] in ['CREATE_FAILED', 'DELETE_FAILED', 'UPDATE_FAILED']:
            failure_message += f"Resource: {event['ResourceType']} - Status: {event['ResourceStatus']} - Reason: {event['ResourceStatusReason']}\n"

    # Request a fix from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a CloudFormation expert."},
            {"role": "user", "content": failure_message}
        ]
    )

    suggested_fix = response.choices[0].message['content']
    print(f"Suggested fix:\n{suggested_fix}")

    # Prompt the user to approve the fix
    approve_fix = input("Do you want to apply this fix? (yes/no): ").strip().lower()
    return approve_fix == "yes", suggested_fix