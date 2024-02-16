import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import pyautogui
import uuid
import csv
import os

class ClickApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_tabs()
        self.check_csv_file()

    def setup_window(self):
        """Initial window setup."""
        self.root.title("Not AFK v3")
        self.root.geometry("450x325")
        self.instance_id = str(uuid.uuid4())

    def setup_tabs(self):
        """Configure tabs for the application."""
        tab_control = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(tab_control)
        self.tab2 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text='Main')
        tab_control.add(self.tab2, text='Summary')
        tab_control.pack(expand=1, fill="both")
        self.setup_tab1()
        self.setup_tab2()

    def setup_tab1(self):
        """Set up the main functionality tab."""
        status_frame = ttk.Frame(self.tab1, padding="10")
        status_frame.pack(fill='both', expand=True)

        self.status_label = ttk.Label(status_frame, text="Status: Stopped", font=("Helvetica", 16))
        self.status_label.pack(pady=10)

        self.total_time_label = ttk.Label(status_frame, text="Total Running Time: 0 seconds")
        self.total_time_label.pack(pady=10)

        button_frame = ttk.Frame(status_frame)
        button_frame.pack(pady=20)

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12))
        style.map('success.TButton', background=[('!disabled', 'green')])
        style.map('danger.TButton', background=[('!disabled', 'red')])

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start, style='success.TButton')
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_and_save, style='danger.TButton')
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.click_count = 0
        self.click_button = ttk.Button(status_frame, text="Click Me", command=self.increment_click_count_and_save)
        self.click_button.pack(pady=10)

        self.click_count_label = ttk.Label(status_frame, text="Click Count: 0")
        self.click_count_label.pack()

        self.running = False
        self.start_time = None
        self.total_running_time = 0

    def setup_tab2(self):
        """Set up the summary tab."""
        summary_frame = ttk.Frame(self.tab2, padding="10")
        summary_frame.pack(fill='both', expand=True, padx=10)

        self.total_seconds_label = ttk.Label(summary_frame, text="Total Seconds: 0", font=("Helvetica", 12), anchor='w')
        self.total_seconds_label.pack(fill='x', pady=5)

        self.total_clicks_label = ttk.Label(summary_frame, text="Total Clicks: 0", font=("Helvetica", 12), anchor='w')
        self.total_clicks_label.pack(fill='x', pady=5)

        self.unique_ids_label = ttk.Label(summary_frame, text="Unique IDs: 0", font=("Helvetica", 12), anchor='w')
        self.unique_ids_label.pack(fill='x', pady=5)

        self.process_button = ttk.Button(summary_frame, text="Process Data", command=self.process_data)
        self.process_button.pack(pady=10)

    def check_csv_file(self):
        """Check and create the CSV file if it does not exist."""
        self.csv_file = r'C:\Users\vzupanic\Desktop\NotAFK\data.csv'
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Seconds Running', 'Click Count'])

    def start(self):
        """Start the click simulation."""
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.status_label.config(text="Status: Running")
            self.start_button.state(['disabled'])
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
            self.update_labels()

    def stop_and_save(self):
        """Stop the click simulation and save data."""
        if self.running:
            self.running = False
            self.start_button.state(['!disabled'])
            self.status_label.config(text="Status: Stopped")
            self.total_running_time += time.time() - self.start_time if self.start_time else 0
            self.start_time = None
            self.save_data()

    def run(self):
        """Simulate clicks at random intervals."""
        while self.running:
            time.sleep(random.randint(1, 120))
            pyautogui.click()

    def update_labels(self):
        """Update the UI labels with the current running time."""
        if self.running:
            elapsed_time = time.time() - self.start_time
            self.total_time_label.config(text=f"Total Running Time: {int(self.total_running_time + elapsed_time)} seconds")
            self.root.after(1000, self.update_labels)

    def increment_click_count_and_save(self):
        """Increment click count and save data."""
        self.click_count += 1
        self.click_count_label.config(text=f"Click Count: {self.click_count}")
        self.save_data()

    def save_data(self):
        """Save the current data to the CSV file."""
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.instance_id, int(self.total_running_time), self.click_count])

    def process_data(self):
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
            fieldnames = ['ID', 'Seconds Running', 'Click Count']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for id, values in data.items():
                writer.writerow({'ID': id, **values})

        total_seconds = sum(item['Seconds Running'] for item in data.values())
        total_clicks = sum(item['Click Count'] for item in data.values())
        unique_ids_count = len(data)

        # Update the labels with the processed data
        self.total_seconds_label.config(text=f"Total Seconds: {total_seconds}")
        self.total_clicks_label.config(text=f"Total Clicks: {total_clicks}")
        self.unique_ids_label.config(text=f"Unique IDs: {unique_ids_count}")


root = tk.Tk()
app = ClickApp(root)
root.mainloop()
