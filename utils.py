import csv
import os
import threading
from datetime import datetime

import winsound


def check_csv_file(csv_file, values):
    """
    Checks for the existence of a CSV file and creates it with specified headers if it does not exist.

    Parameters:
    - csv_file (str): The path to the CSV file.
    - values (list): A list of strings representing the header row's column names for the CSV file.
    """
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(values)


def save_data(csv_file, instance_id, total_running_time, click_count):
    """
    Saves data to the specified CSV file. If `instance_id` is provided, saves data from autoclicker,
    otherwise, saves data from timer.

    Parameters:
    - csv_file (str): The path to the CSV file where data will be saved.
    - instance_id (str): The unique identifier for the data instance. If not provided, a different data format is used.
    - total_running_time (int): The total running time to be recorded. Can also be Seconds Ran for timer.
    - click_count (int): The number of clicks to be recorded. Can also be Total Supposed Time for timer.

    The function adds a date stamp to each entry automatically.
    """
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
    """
    Plays a beep sound in a separate thread, preventing the beep from blocking the main application.

    Parameters:
    - frequency (int): The frequency of the beep sound in Hertz. Default is 440 Hz.
    - duration (int): The duration of the beep sound in milliseconds. Default is 1000 milliseconds (1 second).

    Utilizes `winsound.Beep` for sound generation, wrapped in a threaded function to allow asynchronous execution.
    """
    def threaded_beep():
        winsound.Beep(frequency, duration)

    beep_thread = threading.Thread(target=threaded_beep)
    beep_thread.start()


def format_time(value, unit):
    """
    Formats a time value into a string based on the specified unit.

    Parameters:
    - value (int): The time value to be formatted.
    - unit (str): The unit of time, which can be "minutes" or "seconds". Other values result in a direct string representation.

    Returns:
    - A formatted time string. For "minutes", returns a string in "MM:SS" format. For "seconds", returns a string with "s" suffix. Otherwise, returns the value as a string with the unit.
    """
    if unit == "minutes":
        minutes = int(value) // 60
        seconds = int(value) % 60
        return f"{minutes}:{seconds:02d}"
    elif unit == "seconds":
        return f"{int(value)}s"
    else:
        return f"{value} {unit}"
