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
    notebook.pack(fill='both', expand=True)

    #CREATE SET CREATION TAB
    create_set_frame = ttk.Frame(notebook)
    notebook.add(create_set_frame, text='Create Set')

    #LABEL AND ENTRY WIDGETS FOR SET NAME AND DEFINITION
    ttk.Label(create_set_frame, text='Set Name:').pack(padx=5, pady=5)
    ttk.Entry(create_set_frame, textvariable=set_name_var, width=30).pack(pady=5, padx=5)

    ttk.Label(create_set_frame, text='Word:').pack(padx=5, pady=5)
    ttk.Entry(create_set_frame, textvariable=set_name_var, width=30).pack(pady=5, padx=5)


    ttk.Label(create_set_frame, text='Definition:').pack(padx=5, pady=5)
    ttk.Entry(create_set_frame, textvariable=set_name_var, width=30).pack(pady=5, padx=5)

    #BUTTON TO ADD A WORD TO THE SET


    main_window.mainloop()