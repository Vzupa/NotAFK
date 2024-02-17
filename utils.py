import csv
import os
import threading
from datetime import datetime

import winsound


def check_csv_file(csv_file, values):
    """Check and create the CSV file if it does not exist."""
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(values)


def save_data(csv_file, instance_id, total_running_time, click_count):
    """Save the current data to the CSV file."""
    current_date = datetime.now().strftime('%Y-%m-%d')
    if instance_id:
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([instance_id, current_date, int(total_running_time), click_count])
    else:
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_date, int(total_running_time), click_count])


def beep(frequency=440, duration=1000):
    def threaded_beep():
        winsound.Beep(frequency, duration)

    beep_thread = threading.Thread(target=threaded_beep)
    beep_thread.start()


def format_time(value, unit):
    if unit == "minutes":
        minutes = int(value) // 60
        seconds = int(value) % 60
        return f"{minutes}:{seconds:02d}"
    elif unit == "seconds":
        return f"{int(value)}s"
    else:
        return f"{value} {unit}"