import csv
import boto3
import logging
from termcolor import colored
from datetime import datetime

class DevOpsGuruLogger:
    def __init__(self, log_file="devopsguru.log"):
        self.log_file = log_file
        # Configure CSV file
        with open(self.log_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date and Time", "Event Log", "AWS Account ID"]) # Header

    def log(self, level, message, aws_account_id="N/A"):
        # Add date and time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{timestamp} - {message}"

        # Colorize and print to console
        if level == "info":
            print(colored(formatted_message, 'green'))
            self._write_to_csv(timestamp, message, aws_account_id)
        elif level == "warning":
            print(colored(formatted_message, 'yellow'))
        elif level == "error":
            print(colored(formatted_message, 'red'))

    def _write_to_csv(self, timestamp, message, aws_account_id):
        # Write to CSV file
        with open(self.log_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, message, aws_account_id])

log = DevOpsGuruLogger()