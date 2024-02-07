import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import style

if __name__ == '__main__':

    #CREATING MAIN WINDOW
    main_window = tk.Tk()
    main_window.title("Flashcard App")
    main_window.geometry('500x400')

    #APPLY STYLING TO GUI
    decor = style(theme='superhero')
    decor.configure('TLabel', font= ('TkDefaultFont', 18))
    decor.configure('TButton', font= ('TkDefaultFont', 16))

    main_window.mainloop()