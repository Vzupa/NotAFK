import csv
import os
from datetime import datetime


def check_csv_file(csv_file):
    """Check and create the CSV file if it does not exist."""
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Date', 'Seconds Running', 'Click Count'])


def save_data(csv_file, instance_id, total_running_time, click_count):
    """Save the current data to the CSV file."""
    current_date = datetime.now().strftime('%Y-%m-%d')

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([instance_id, current_date, int(total_running_time), click_count])
