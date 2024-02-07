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
    style = Style(theme='superhero')
    style.configure('TLabel', font= ('TkDefaultFont', 18))
    style.configure('TButton', font= ('TkDefaultFont', 16))

    #STORING USER INPUTS ON VARIABLES
    set_name_var = tk.StringVar()
    word_var = tk.StringVar()
    definition_var = tk.StringVar()

    #NOTEBOOK WIDGET FOR MANAGING TABS
    notebook = ttk.Notebook(main_window)

    main_window.mainloop()