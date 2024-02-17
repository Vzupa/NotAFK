import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import pyautogui
from utils import save_data
from file_paths import afk_csv


class AutoClicker:
    def __init__(self, frame, instance_id):
        self.frame = frame
        self.instance_id = instance_id
        self.click_count = 0
        self.running = False
        self.start_time = None
        self.total_running_time = 0
        self.setup_tab()

    def setup_tab(self):
        """Set up the main functionality tab."""
        status_frame = ttk.Frame(self.frame, padding="10")
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

        self.click_button = ttk.Button(status_frame, text="Click Me", command=self.increment_click_count_and_save)
        self.click_button.pack(pady=10)

        self.click_count_label = ttk.Label(status_frame, text="Click Count: 0")
        self.click_count_label.pack()

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
            save_data(afk_csv, self.instance_id, self.total_running_time, self.click_count)

    def run(self):
        """Simulate clicks at random intervals."""
        while self.running:
            time.sleep(random.randint(1, 120))
            pyautogui.click()

    def update_labels(self):
        """Update the UI labels with the current running time."""
        if self.running:
            elapsed_time = time.time() - self.start_time
            self.total_time_label.config(
                text=f"Total Running Time: {int(self.total_running_time + elapsed_time)} seconds")
            self.frame.after(1000, self.update_labels)

    def increment_click_count_and_save(self):
        """Increment click count and save data."""
        self.click_count += 1
        self.click_count_label.config(text=f"Click Count: {self.click_count}")
        save_data(afk_csv, self.instance_id, self.total_running_time, self.click_count)
