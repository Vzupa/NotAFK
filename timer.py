import tkinter as tk
import random
from tkinter import ttk
from utils import beep, format_time, save_data
from file_paths import timer_csv


class Timer:
    def __init__(self, master, csv_file=None, instance_id=None):
        self.first_beep = True
        self.values = {}
        self.scales = []
        self.initial_time = 5 * 60
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        self.timer_label = ttk.Label(self.master, text="05:00", font=("Helvetica", 24))
        self.timer_label.pack(pady=5)

        self.scale = tk.Scale(self.master, from_=5, to=120, orient=tk.HORIZONTAL, length=400, sliderlength=30, width=20,
                              command=self.update_timer, showvalue=False)
        self.scale.pack(pady=10)

        self.start_stop_button = ttk.Button(self.master, text="Start", command=self.toggle_timer)
        self.start_stop_button.pack(pady=10)

        self.setup_gap_settings()

        self.timer_running = False
        self.time_left = 300

    def setup_gap_settings(self):
        timer_settings = [
            ("Minimum Interval", 5 * 60, 19 * 60, 30, 5 * 60, "minutes"),
            ("Duration", 5, 15, 1, 10, "seconds"),
            ("Maximum Interval", 6 * 60, 20 * 60, 30, 5 * 60, "minutes")
        ]

        for label_text, from_val, to_val, step, initial_val, unit in timer_settings:
            frame = ttk.Frame(self.master)
            ttk.Label(frame, text=label_text).pack()

            initial_text = format_time(initial_val, unit)
            timer_label = ttk.Label(frame, text=initial_text, font=("Helvetica", 12))
            timer_label.pack(pady=10)

            scale = ttk.Scale(frame, from_=from_val, to_=to_val, orient=tk.HORIZONTAL,
                              command=lambda value, lbl=timer_label, lt=label_text, stp=step, unt=unit:
                              self.update_timer_scale(value, lbl, lt, stp, unt))
            scale.set(initial_val)
            scale.pack()
            frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            self.scales.append(scale)
            self.values[label_text] = initial_val

    def update_timer_scale(self, value, timer_label, label_text, step, unit):
        rounded_value = round(float(value) / step) * step
        self.values[label_text] = rounded_value
        formatted_time = format_time(rounded_value, unit)
        timer_label.config(text=formatted_time)

    def update_timer(self, value):
        nearest_five = round(float(value) / 5) * 5
        self.time_left = int(nearest_five * 60)
        self.initial_time = int(nearest_five * 60)

        current_scale_value = round(self.scale.get() / 5) * 5
        if current_scale_value != nearest_five:
            self.scale.set(nearest_five)

        self.timer_label.config(text=f"{int(self.time_left / 60):02d}:{self.time_left % 60:02d}")

    def toggle_timer(self):
        if self.timer_running:
            self.stop_timer()
        else:
            self.validate_and_adjust_intervals()
            self.start_timer()

    def start_timer(self):
        self.timer_running = True
        self.start_stop_button.config(text="Stop")
        self.scale.config(state=tk.DISABLED)
        for scale in self.scales:
            scale.config(state=tk.DISABLED)
        self.calculate_next_beep()
        self.countdown()

    def stop_timer(self):
        self.timer_running = False
        self.start_stop_button.config(text="Start")
        self.scale.config(state=tk.NORMAL)
        for scale in self.scales:
            scale.config(state=tk.NORMAL)

        save_data(timer_csv, None, self.initial_time - self.time_left, self.initial_time)
        self.scale.set(self.initial_time / 60)
        self.time_left = self.initial_time

    def countdown(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"{int(self.time_left / 60):02d}:{self.time_left % 60:02d}")
            if self.time_left == self.next_beep_time:
                beep(1000, 400)
                self.calculate_next_beep()
            self.master.after(1000, self.countdown)
        else:
            self.stop_timer()

    def calculate_next_beep(self):
        if self.timer_running and self.first_beep:
            min_interval = self.values.get("Minimum Interval", 60)
            max_interval = self.values.get("Maximum Interval", 120)
            beep_interval = random.randint(min_interval, max_interval)
            self.next_beep_time = max(0, self.time_left - beep_interval)
            self.first_beep = False
        elif self.timer_running and not self.first_beep:
            self.next_beep_time = self.time_left - self.values["Duration"]
            self.first_beep = True

    def validate_and_adjust_intervals(self):
        min_value = self.values.get("Minimum Interval", 0)
        max_value = self.values.get("Maximum Interval", 0)

        if min_value > max_value:
            self.values["Minimum Interval"], self.values["Maximum Interval"] = max_value, min_value
        elif min_value == max_value:
            self.values["Minimum Interval"] = max_value - 30
            self.values["Maximum Interval"] = min_value + 30

        self.scales[0].set(self.values["Minimum Interval"])
        self.scales[2].set(self.values["Maximum Interval"])
