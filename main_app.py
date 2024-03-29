import tkinter as tk
from tkinter import ttk
import uuid
from autoclicker import AutoClicker
from summarizer import Summarizer
from timer import Timer
from utils import check_csv_file
from file_paths import afk_csv, timer_csv


class ClickApp:
    def __init__(self, root):
        self.csv_file = afk_csv
        check_csv_file(self.csv_file, ['ID', 'Date', 'Seconds Running', 'Click Count'])
        check_csv_file(timer_csv, ['Date', 'Seconds Ran', 'Total Time'])
        self.instance_id = str(uuid.uuid4())
        self.root = root
        self.setup_window()
        self.setup_tabs()

    def setup_window(self):
        self.root.title("Not AFK v3")
        self.root.geometry("450x325")

    def setup_tabs(self):
        tab_control = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(tab_control)
        self.tab2 = ttk.Frame(tab_control)
        self.tab3 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text='AutoClicker')
        tab_control.add(self.tab2, text='Timer')
        tab_control.add(self.tab3, text='Summary')
        tab_control.pack(expand=1, fill="both")

        AutoClicker(self.tab1, self.instance_id)
        Timer(self.tab2)
        Summarizer(self.tab3)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClickApp(root)
    root.mainloop()
