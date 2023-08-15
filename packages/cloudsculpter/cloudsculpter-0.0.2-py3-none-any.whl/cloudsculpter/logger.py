import csv
import logging
from termcolor import colored
from datetime import datetime

class CSVHandler(logging.Handler):
    def __init__(self, log_file="cloudsculpter.log"):
        super().__init__()
        self.log_file = log_file
        # Configure CSV file
        with open(self.log_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date and Time", "Event Log", "AWS Account ID"]) # Header

    def emit(self, record):
        # Write to CSV file
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, record.msg, "N/A"]) # Change "N/A" if AWS Account ID is available

class CloudSculpterLogger:
    def __init__(self):
        self.logger = logging.getLogger('CloudSculpter')
        self.logger.setLevel(logging.INFO)
        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(ColoredFormatter())
        self.logger.addHandler(ch)
        # CSV handler
        csv_handler = CSVHandler()
        self.logger.addHandler(csv_handler)

class ColoredFormatter(logging.Formatter):
    COLORS = {'INFO': 'green', 'WARNING': 'yellow', 'ERROR': 'red'}

    def format(self, record):
        log_message = super().format(record)
        return colored(log_message, self.COLORS.get(record.levelname))

# Usage example
log = CloudSculpterLogger().logger