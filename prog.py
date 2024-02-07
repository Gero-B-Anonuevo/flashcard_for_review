import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Style

#CREATE DATABASE TABLES
def create_tables(conn):
    cursor = conn.cursor()

    #CREATE FLASHCARD SETS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcard_sets (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL
        )
    ''')

    #CREATE FLASHCARDS TABLE WITH FOREIGN KEY REFERENCE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcard (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   set_id INTEGER NOT NULL,
                   word TEXT NOT NULL,
                   definition TEXT NOT NULL,
                   FOREIGN KEY (set_id) REFERENCES flashcard_sets(id)
        )
    ''')

#ADD NEW FLASHCARD TO THE DATABASE
def add_set(conn, name):
    cursor = conn.cursor()

    #INSERT THE SET NAME INTO flashcard_sets table
    cursor.execute('''
        INSERT INTO flashcard_sets (name)
        VALUES (?)
    ''', (name,))

    set_id = cursor.lastrowid
    conn.commit()

    return set_id

if __name__ == '__main__':
    #CONNECT TO SQLITE DATABASE AND CREATE TABLES
    conn = sqlite3.connect('flashcard.db')
    create_tables(conn)

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
    ttk.Entry(create_set_frame, textvariable=word_var, width=30).pack(pady=5, padx=5)


    ttk.Label(create_set_frame, text='Definition:').pack(padx=5, pady=5)
    ttk.Entry(create_set_frame, textvariable=definition_var, width=30).pack(pady=5, padx=5)

    #BUTTON TO ADD A WORD TO THE SET
    ttk.Button(create_set_frame, text='Add Word').pack(pady=10, padx=5)

    #BUTTON TO SAVE THE SET
    ttk.Button(create_set_frame, text='Save Set').pack(pady=10, padx=5)

    #CREATING SET SELECTION TAB
    set_selection_frame = ttk.Frame(notebook)
    notebook.add(set_selection_frame, text='Select Set')

    #COMBOBOX FOR SELECTING EXISTING SETS
    sets_combobox = ttk.Combobox(set_selection_frame, state='readonly')
    sets_combobox.pack(padx=5, pady=40)

    #BUTTON TO SELECT SET
    ttk.Button(set_selection_frame, text='Select Set').pack(padx=5, pady=5)

    #BUTTON TO DELETE SET
    ttk.Button(set_selection_frame, text='Deleet Set').pack(padx=5, pady=5)

    #CREATING LEARN MODE TAB
    flashcards_frame = ttk.Frame(notebook)
    notebook.add(flashcards_frame, text='Learn Mode')

    #INITIALIZE VARIABLES FOR TRACKING CARD INDEX AND CURRENT CARD
    card_index = 0
    current_tabs = []

    #LABEL TO DISPLAY THE WORD ON FLASHCARD
    word_label = ttk.Label(flashcards_frame, text='', font=('TkDefaultFont', 24))
    word_label.pack(padx=5, pady=40)

    #LABEL TO DISPLAY THE DEFINITION ON FLASHCARDS
    definition_label = ttk.Label(flashcards_frame, text='')
    definition_label.pack(padx=5, pady=5)

    #BUTTON TO FLIP FLASH CARD
    ttk.Button(flashcards_frame, text='Flip').pack(side='left', padx=5, pady=5)

    #BUTTON TO VIEW NEXT FLASHCARD
    ttk.Button(flashcards_frame, text='Next').pack(side='right', padx=5, pady=5)

    #BUTTON TO VIEW THE PREVIOUS FLASHCARD
    ttk.Button(flashcards_frame, text='Previous').pack(side='right', padx=5, pady=5)

    #populate_sets_combobox

    main_window.mainloop()