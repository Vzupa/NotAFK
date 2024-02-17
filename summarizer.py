from tkinter import ttk
import csv
from file_paths import timer_csv


class Summarizer:
    def __init__(self, frame, csv_file):
        self.frame = frame
        self.csv_file = csv_file
        self.setup_tab()

    def setup_tab(self):
        """Set up the summary tab."""
        summary_frame = ttk.Frame(self.frame, padding="10")
        summary_frame.pack(fill='both', expand=True, padx=10)

        autocliker_frame = ttk.Frame(self.frame, padding="10")
        autocliker_frame.pack(fill='both', expand=True, padx=10)

        self.total_seconds_label = ttk.Label(autocliker_frame, text="Total Seconds: 0", font=("Helvetica", 12), anchor='w')
        self.total_seconds_label.pack(fill='x', pady=5)

        self.total_clicks_label = ttk.Label(autocliker_frame, text="Total Clicks: 0", font=("Helvetica", 12), anchor='w')
        self.total_clicks_label.pack(fill='x', pady=5)

        self.unique_ids_label = ttk.Label(autocliker_frame, text="Unique IDs: 0", font=("Helvetica", 12), anchor='w')
        self.unique_ids_label.pack(fill='x', pady=5)

        timer_frame = ttk.Frame(self.frame, padding="10")
        timer_frame.pack(fill='both', expand=True, padx=10)

        self.total_actual_time = ttk.Label(timer_frame, text="Total Actual Time: 0", font=("Helvetica", 12), anchor='w')
        self.total_actual_time.pack(fill='x', pady=5)

        self.total_supposed_time = ttk.Label(timer_frame, text="Total Supposed Time: 0", font=("Helvetica", 12), anchor='w')
        self.total_supposed_time.pack(fill='x', pady=5)

        self.unique_tries_label = ttk.Label(timer_frame, text="Unique Tries: 0", font=("Helvetica", 12), anchor='w')
        self.unique_tries_label.pack(fill='x', pady=5)

        self.process_button = ttk.Button(summary_frame, text="Process Data", command=self.process_data)
        self.process_button.pack(pady=10)

    def process_data(self):
        self.process_AFK_data()
        self.process_timer_data()

    def process_AFK_data(self):
        """Process the data for summary."""
        data = {}
        with open(self.csv_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row['ID']
                seconds = int(row['Seconds Running'])
                clicks = int(row['Click Count'])
                if id not in data or data[id]['Seconds Running'] < seconds:
                    data[id] = {'Seconds Running': seconds, 'Click Count': clicks}

        with open(self.csv_file, mode='w', newline='') as file:
            fieldnames = ['ID', 'Date', 'Seconds Running', 'Click Count']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for id, values in data.items():
                writer.writerow({'ID': id, **values})

        total_seconds = sum(item['Seconds Running'] for item in data.values())
        total_clicks = sum(item['Click Count'] for item in data.values())
        unique_ids_count = len(data)

        self.total_seconds_label.config(text=f"Total Seconds: {total_seconds}")
        self.total_clicks_label.config(text=f"Total Clicks: {total_clicks}")
        self.unique_ids_label.config(text=f"Unique IDs: {unique_ids_count}")

    def process_timer_data(self):
        filtered_data = []
        total_seconds_ran = 0
        total_time = 0
        row_count = 0

        with open(timer_csv, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if int(row[1]) != 0:
                    filtered_data.append(row)
                    total_seconds_ran += int(row[1])
                    total_time += int(row[2])
                    row_count += 1

        with open(timer_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(filtered_data)

        self.total_actual_time.config(text=f"Total Actual Time: {total_seconds_ran}")
        self.total_supposed_time.config(text=f"Total Supposed Time: {total_time}")
        self.unique_tries_label.config(text=f"Unique Tries: {row_count}")
