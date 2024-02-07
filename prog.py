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

#FUNCTION TO ADD FLASHCARD TO DATABASE
def add_card(conn, set_id, word, definition):
    cursor = conn.cursor()

    #EXECUTE SQL QUERY TO INSERT A NEW FLASHCARD INTO THE DATABASE
    cursor.execute('''
        INSERT INTO flashcards (set_id, word, definition)
        VALUES (?, ?, ?)
    ''', (set_id, word, definition))

    #GET THE ID OF THE NEWLY INSERTED CARD
    card_id = cursor.lastrowid
    conn.commit()

    return card_id

#FUNTION TO RETRIEVE ALL FLASHCARD SETS FROM THE DATABASE
def get_sets(conn):
    cursor = conn.cursor()

    #EXECUTE SQL QUERY TO FETCH ALL FLASHCARD SETS
    cursor.execute('''
        SELECT id, name FROM flashcard_sets
    ''')

    rows= cursor.fetchall()
    sets={row[1]: row[0] for row in rows}

    return sets
#FUNCTION TO RETRIEVE ALL FLASHCARDS OF A SPECIFIC SET
def get_cards(conn, set_id):
    cursor = conn.cursor()

    cursor.execute('''
        SELECT word, definition FROM flashcards
        WHERE set_id = ?
    ''', (set_id,))

    rows = cursor.fetchall()
    cards = [(row[0], row[1]) for row in rows]

    return cards

#FUNCTION TO DELETE FLASHCARD SET FROM DATABASE
def delete_set(conn, set_id):
    cursor = conn.cursor()

    #EXECUTE SQL QUERY TO DELETE A FLASHCARD SET
    cursor.execute('''
        DELETE FROM flashcard_sets
        WHERE id = ?
    ''', (set_id,))

    conn.commit()
    sets_combobox.set('')
    clear_flashcard_display()
    populate_sets_combobox()

    #CLEAR current_cards LIST AND RESET card_index
    global current_cards, card_index
    current_cards = []
    card_index = 0

#FUNCTION TO CREATE NEW FLASHCARD SET
def create_set():
    set_name = set_name_var.get()
    if set_name:
        if set_name not in get_sets(conn):
            set_id = add_set(conn, set_name)
            populate_sets_combobox()
            set_name_var.set('')

            #CLEAR THE INPUT FIELDS
            set_name_var.set('')
            word_var.set('')
            definition_var.set('')

def add_word():
    set_name = set_name_var.get()
    word = word_var.get()
    definition = definition_var.get()

    if set_name and word and definition:
        if set_name not in get_sets(conn):
            set_id = add_set(conn, set_name)
        else:
            set_id = get_sets(conn)[set_name]

        add_card(conn, set_id, word, definition)

        word_var.set('')
        definition_var.set('')

        populate_sets_combobox()

def populate_sets_combobox():
    sets_combobox['values'] = tuple(get_sets(conn).keys())

#FUNCTION TO DELETE A SELECTED FLASHCARD SET
def delete_selected_set():
    set_name = sets_combobox.get()

    if set_name:
        result = messagebox.askyesno('Confirmation', f'Are you sure you want to delete the "{set_name}" set?')

        if result == tk.YES:
            set_id = get_sets(conn)[set_name]
            delete_set(conn, set_id)
            populate_sets_combobox()
            clear_flashcard_display()

def select_set():
    set_name = sets_combobox.get()

    if set_name:
        set_id = get_sets(conn)[set_name]
        cards = get_cards(conn, set_id)

        if cards:
            display_flashcards(cards)
        else:
            word_label.config(text="No cards in this set")
            definition_label.config(text='')
    else:
        #CLEAR THE CURRENT CARDS LIST AND RESET CARD INDEX
        global current_cards, card_index
        current_cards = []
        card_index = 0
        clear_flashcard_display()

def display_flashcards(cards):
    global card_index, current_cards
    card_index=0
    current_cards = cards

    #CLEAR DISPLAY
    if not cards:
        clear_flashcard_display()
    else:
        show_card()
    show_card()

def clear_flashcard_display():  
    word_label.config(text='')
    definition_label.config(text='')

#FUNCTION TO DISPLAY THE CURRENT FLASHCARDS WORD
def show_card():
    global card_index, current_cards

    if current_cards:
        if 0 <= card_index < len(current_cards):
            word, _ = current_cards[card_index]
            word_label.config(text=word)
            definition_label.config(text='')
        else:
            clear_flashcard_display()
    else:
        clear_flashcard_display()

#FUNCTION TO FLIP THE CURRENT CARD AND DISPLAY ITS DEFINITION
def flip_card():
    global card_index, current_cards

    if current_cards:
        _, definition = current_cards[card_index]
        definition_label.config(text=definition)

#FUNCTION TO MOVE TO THE NEXT CARD
def next_card():
    global card_index, current_cards

    if current_cards:
        card_index = min(card_index + 1, len(current_cards) -1)
        show_card()

#FUNCTION TO MOVE TO THE PREVIOUS CARD
def previous_card():
    global card_index, current_cards

    if current_cards:
        card_index = max(card_index - 1, 0)
        show_card()


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
    ttk.Button(create_set_frame, text='Add Word', command=add_word).pack(pady=10, padx=5)

    #BUTTON TO SAVE THE SET
    ttk.Button(create_set_frame, text='Save Set', command=create_set).pack(pady=10, padx=5)

    #CREATING SET SELECTION TAB
    set_selection_frame = ttk.Frame(notebook)
    notebook.add(set_selection_frame, text='Select Set')

    #COMBOBOX FOR SELECTING EXISTING SETS
    sets_combobox = ttk.Combobox(set_selection_frame, state='readonly')
    sets_combobox.pack(padx=5, pady=40)

    #BUTTON TO SELECT SET
    ttk.Button(set_selection_frame, text='Select Set', command=select_set).pack(padx=5, pady=5)

    #BUTTON TO DELETE SET
    ttk.Button(set_selection_frame, text='Deleet Set', command=delete_selected_set).pack(padx=5, pady=5)

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
    ttk.Button(flashcards_frame, text='Flip', command=flip_card).pack(side='left', padx=5, pady=5)

    #BUTTON TO VIEW NEXT FLASHCARD
    ttk.Button(flashcards_frame, text='Next', command=next_card).pack(side='right', padx=5, pady=5)

    #BUTTON TO VIEW THE PREVIOUS FLASHCARD
    ttk.Button(flashcards_frame, text='Previous', command=previous_card).pack(side='right', padx=5, pady=5)

    populate_sets_combobox

    main_window.mainloop()