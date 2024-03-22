from tkinter import *
import tkinter as tk
from configparser import ConfigParser

class EditPomodoroTimer:
    def __init__(self, update):
        top = tk.Toplevel()
        self.frame = Frame(top)
        self.update = update
        #top.wm_iconbitmap(bitmap=logo_path) disable for ortogonalność
        top.title("Edit Pomodoro Timer")
        top.geometry("500x200+460+350")
        
        self.get_value_from_file()
        self.create_widgets(top)
        
    def get_value_from_file(self):
        self.config = ConfigParser()
        self.config.read("./settings/config.ini")
        self.pomodoro_time = tk.StringVar(value=self.config.get("Settings", "pomodoro_time", fallback="25"))
        self.short_break_time = tk.StringVar(value=self.config.get("Settings", "short_break_time", fallback="5"))
        self.long_break_time = tk.StringVar(value=self.config.get("Settings", "long_break_time", fallback="15"))

    def create_widgets(self, parent):
        pomodoro_label = tk.Label(parent, text="Pomodoro", font=("Helvetica", 12))
        pomodoro_label.pack()

        pomodoro_entry = tk.Entry(parent, textvariable=self.pomodoro_time)
        pomodoro_entry.pack(padx=5, pady=5)
        pomodoro_entry.focus()

        short_break_label = tk.Label(parent, text="Short Break", font=("Helvetica", 12))
        short_break_label.pack()

        short_break_entry = tk.Entry(parent, textvariable=self.short_break_time)
        short_break_entry.pack(padx=5, pady=5)

        long_break_label = tk.Label(parent, text="Long Break", font=("Helvetica", 12))
        long_break_label.pack()

        long_break_entry = tk.Entry(parent, textvariable=self.long_break_time)
        long_break_entry.pack(padx=5, pady=5)

        save_button = tk.Button(parent, text="Save", command=self.save_values)
        save_button.pack()

    def close_window(self):
        self.frame.master.deiconify()
        self.frame.master.destroy()

    def save_values(self):
        # Save values to the configuration file with a section header
        self.config["Settings"] = {
            "pomodoro_time": self.pomodoro_time.get(),
            "short_break_time": self.short_break_time.get(),
            "long_break_time": self.long_break_time.get(),
        }
    
        # Save the configuration to the file
        with open("./settings/config.ini", "w") as config_file:
            self.config.write(config_file)
            
        self.update()
        self.close_window()
                            
    def close_window(self):
        self.frame.master.deiconify()
        self.frame.master.destroy()