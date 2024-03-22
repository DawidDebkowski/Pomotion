import tkinter as tk

class WhatIsPomodoro:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("What is Pomodoro?")
        #self.window.wm_iconbitmap(bitmap=logo_path) - orto
        self.window.resizable(False, False)
        # Add content to the new window as needed
        descrpition_text = """ 
        The Pomodoro Technique is a time management method that uses a timer to break work into intervals, traditionally 25 minutes in length, separated by short breaks.\n
        The technique aims to improve productivity by reducing distractions and promoting focus and concentration.
        """
        what_is_pom_label = tk.Label(self.window, text=descrpition_text)
        what_is_pom_label.pack()

class HowToPomodoro:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Edit Pomodoro Timer")
        #self.window.wm_iconbitmap(bitmap=logo_path) - orto
        self.window.resizable(False, False) 
        text_how_to = """
        1) Decide task to be done set timers to 25 minutes for one "Pomodoro" \n
        2) Work on task until timer is complete \n
        3) Take a 5 minutes short break \n
        4) After four "Pomodoro" take a long break \n
        5) Repeat to step 1 \n
         
        Final Result: You have worked for 100 minutes and took 15 minutes break"""
        how_to_pomodoro_label = tk.Label(self.window, text=text_how_to)
        how_to_pomodoro_label.pack()