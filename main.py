import sys
from playsound import playsound
import tkinter as tk
import time
from tkinter import *
from configparser import ConfigParser
import os
import requests
from legacy import WhatIsPomodoro, HowToPomodoro
from EditPomodoroTimer import EditPomodoroTimer

class PomodoroTimer:
    def __init__(self):
        self.response = requests.get('https://api.quotable.io/random')
        self.timer_running = False
        self.window = tk.Tk()
        self.window.title("Tomato Timer")
        global logo_path
        logo_path = PomodoroTimer.resource_path(os.path.join('images', 'logo.ico'))
        self.window.wm_iconbitmap(bitmap=logo_path)
        self.seconds = 0
        self.remaining_time = -1
        self.pomodoro_counter = 0
        self.window.geometry("500x250+660+300")
        self.window.resizable(False, False)
        self.mode_selected = ""

        self.create_menu()
        self.get_value_from_file()
        self.create_widgets()
        self.disable_timer_buttons()
        
    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def get_value_from_file(self):
        self.config = ConfigParser()
        self.config.read("./settings/config.ini")
        self.pomodoro_time = tk.StringVar(value=self.config.get("Settings", "pomodoro_time", fallback="25"))
        self.short_break_time = tk.StringVar(value=self.config.get("Settings", "short_break_time", fallback="5"))
        self.long_break_time = tk.StringVar(value=self.config.get("Settings", "long_break_time", fallback="15"))

    def create_menu(self):
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=file_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Edit Pomodoro Timer", command=self.open_edit_pomodoro)
        file_menu.add_command(label="What is pomodoro?", command=self.open_what_is_pomodoro)
        file_menu.add_command(label="How to use pomodoro timer", command=self.open_how_pomodoro)

    def create_widgets(self):     
        frame_mode_buttons = tk.Frame(self.window,padx=10, pady=10)
        frame_mode_buttons.pack()
        
        self.pomodoro_button = tk.Button(frame_mode_buttons, text="Pomodoro", command=self.pomodoro_button_clicked)
        self.pomodoro_button.pack(side="left", padx=5)
        self.short_break_button = tk.Button(frame_mode_buttons, text="Short Break", command=self.short_break_button_clicked)
        self.short_break_button.pack(side="left", padx=5)
        self.long_break_button = tk.Button(frame_mode_buttons, text="Long Break", command=self.long_break_button_clicked)
        self.long_break_button.pack(side="left", padx=5)
        
        self.label = tk.Label(self.window, text="Select your mode!",font=("Helvetica", 14))
        self.label.pack()
        self.text_box = tk.Text(self.window, height=3, width=40)
        if self.response.status_code == 200:
            content = self.response.json()['content']
        else:
            content = "You don’t have to be great to start, but you have to start to be great."
        #self.text_box.insert(tk.END, "You don’t have to be great to start, but you have to start to be great.")
        self.text_box.insert(tk.END, content)
        self.text_box.configure(state=DISABLED)        
        self.text_box.pack()
        
        self.play_photo = tk.PhotoImage(file = PomodoroTimer.resource_path(os.path.join('images', 'play.png')))
        self.pause_photo = tk.PhotoImage(file = PomodoroTimer.resource_path(os.path.join('images', 'pause.png')))
        self.reload_photo = tk.PhotoImage(file = PomodoroTimer.resource_path(os.path.join('images', 'reload.png')))
                        
        frame_buttons_time = tk.Frame(self.window,padx=10, pady=10, height=100, width=100)
        frame_buttons_time.pack()
        self.start_button = tk.Button(frame_buttons_time, text="Start", command=self.start_timer,image=self.play_photo)
        self.start_button.pack(side="left", padx=5)
        self.stop_button = tk.Button(frame_buttons_time, text="Stop", command=self.stop_timer,image=self.pause_photo)
        self.stop_button.pack(side="left", padx=5)
        self.reload = tk.Button(frame_buttons_time, text="Stop", command=self.reload_timer,image=self.reload_photo)
        self.reload.pack(side="left", padx=5)
        
        self.pomodoro_counter_label = tk.Label(self.window, text=f"Pomodoro completed: {self.pomodoro_counter}", font=("Helvetica", 8))
        self.pomodoro_counter_label.pack()
        
    def pomodoro_button_clicked(self):
        pomodoro_value = self.pomodoro_time.get()
        self.set_timer(pomodoro_value)
        self.mode_selected = "Pomodoro"
        self.label.config(text=f"Time remaining: {pomodoro_value} minutes", font=("Helvetica", 14))
        self.enable_timer_buttons()      
        
    def short_break_button_clicked(self):
        short_break_value = self.short_break_time.get()
        self.set_timer(short_break_value)
        self.mode_selected = "short_break"
        self.label.config(text=f"Time remaining: {short_break_value} minutes", font=("Helvetica", 14))
        self.enable_timer_buttons()

    def long_break_button_clicked(self):
        long_break_value = self.long_break_time.get()
        self.set_timer(long_break_value)
        self.mode_selected = "long_break"
        self.label.config(text=f"Time remaining: {long_break_value} minutes", font=("Helvetica", 14))
        self.enable_timer_buttons()

    def set_timer(self, minutes):
        self.seconds = int(minutes) * 60
        self.remaining_time = -1 
        
    def open_what_is_pomodoro(self):
        WhatIsPomodoro(self.window)
        
    def open_edit_pomodoro(self):
        editPomodoroTimer = EditPomodoroTimer(self.update)
        
    def open_how_pomodoro(self):
        HowToPomodoro(self.window)
        
    def start_timer(self):
        if not self.timer_running:
            self.disable_buttons()
            self.timer_running = True
            # Only set start_time if timer is starting fresh or resuming
            if self.remaining_time == -1:
                self.remaining_time = self.seconds
            self.start_time = time.time()  # Capture the start moment
            self.update_timer_label()
            self.stop_button.config(state=tk.NORMAL)

    def update_timer_label(self):
        # Calculate elapsed time since timer (re)started
        elapsed_time = int(time.time() - self.start_time)
        # Adjust remaining time based on elapsed
        current_remaining = max(0, self.remaining_time - elapsed_time)
        
        if self.timer_running and current_remaining > 0:
            minutes, seconds = divmod(current_remaining, 60)
            self.label.config(text=f"Time remaining: {minutes}:{seconds:02d} minutes", font=("Helvetica", 14))
            self.window.after(1000, self.update_timer_label)  # Schedule next update
        elif current_remaining == 0 and self.timer_running:
            self.timer_finished()  # Handle timer finished logic
            
    def timer_finished(self):
        self.timer_running = False
        self.label.config(text="Time finished!")
        if self.mode_selected == "Pomodoro":
            self.pomodoro_counter += 1
            self.pomodoro_counter_label.config(text=f"Pomodoro completed: {self.pomodoro_counter}", font=("Helvetica", 8))
        playsound('./audio/notification.mp3')
        self.enable_buttons()
        self.remaining_time = -1  # Reset remaining time for next round

    def stop_timer(self):
        if self.timer_running:
            # Calculate and save the remaining time
            self.remaining_time -= int(time.time() - self.start_time)
            self.remaining_time = max(0, self.remaining_time)  # Ensure it's not negative
            self.timer_running = False
            self.enable_buttons()
            self.stop_button.config(state=tk.DISABLED)
        
    def reload_timer(self):
        self.stop_timer()
        self. remaining_time = -1
        if self.mode_selected == "Pomodoro":
            self.pomodoro_button_clicked()
        elif self.mode_selected == "short_break":
            self.short_break_button_clicked()
        elif self.mode_selected == "long_break":
            self.long_break_button_clicked()
        
    def enable_buttons(self):
        self.pomodoro_button.config(state=tk.NORMAL)
        self.long_break_button.config(state=tk.NORMAL)
        self.short_break_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)

    def disable_buttons(self):
        self.pomodoro_button.config(state=tk.DISABLED)
        self.long_break_button.config(state=tk.DISABLED)
        self.short_break_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)
        
    def disable_timer_buttons(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.reload.config(state=tk.DISABLED)
        
    def enable_timer_buttons(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        self.reload.config(state=tk.NORMAL)

    def update(self):
        self.get_value_from_file()
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    timer = PomodoroTimer()
    timer.window.mainloop()

    