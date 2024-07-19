import tkinter as tk
from tkinter import scrolledtext, messagebox
from deque import *
import itertools
import sys
from collections import deque
from nltk.grammar import CFG, Nonterminal
from grammar import grammar_list

from tkinter import ttk


# Fonction de validation des entiers
def validate_integer(P):
    return P.isdigit() or P == ""

# Vérifie si un champ est vide
def is_empty():
    if len(textbox.get("1.0", tk.END).strip()) == 0 or len(entry.get()) == 0:
        messagebox.showwarning("Erreur", "Veuillez renseigner tous les champs.")
        return True    
    return False

# Récupère la grammaire depuis le textbox
def get_grammar():
    if is_empty():
        return
    grammar_text = textbox.get("1.0", tk.END).strip()
    const = int(entry.get())
    
    constraints = {}
    for constraint in constraint_listbox.get(0, tk.END):
        terminal, limit = constraint.split(':')
        constraints[terminal.strip()] = int(limit.strip())
    
    # La ligne suivante dépend de votre importation réelle de CFG
    grammar = CFG.fromstring(grammar_text)
    words = list(generate_iterative(grammar, max_length=const))
    
    filtered_words = [word for word in words if all(word.count(t) <= constraints[t] for t in constraints)]
    
    Listbox_result.delete(0, tk.END)
    for n, sent in enumerate(filtered_words, 1):
        Listbox_result.insert(tk.END, f"{n:3d}. {sent}")

# Définit la grammaire usuelle
def set_grammar(index):
    textbox.delete("1.0", tk.END)
    textbox.insert(tk.END, grammar_list[index].strip())

# Efface le texte du textbox
def clear():
    textbox.delete("1.0", tk.END)

# Ajoute une contrainte à la liste des contraintes
def add_constraint():
    terminal = terminal_combobox.get()
    limit = limit_entry.get()
    if terminal and limit:
        constraint_listbox.insert(tk.END, f"{terminal}: {limit}")
        terminal_combobox.set('')
        limit_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un terminal et entrer une limite.")

# Création de la fenêtre principale
root = tk.Tk()
root.geometry("800x600")
root.title("Grammar Generator")

# Titre principal
label = tk.Label(root, text="Welcome to Grammar Generator", font=('Arial', 18, 'italic'), fg='navy')
label.pack(padx=20, pady=20)

# Frame pour les boutons à droite
btn_frame = tk.Frame(root)
btn_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)

label_ram = tk.Label(btn_frame, text="Grammaires usuelles:", font=('Arial', 12, 'bold'))
label_ram.pack(pady=10)

# Style commun pour les boutons
button_style = {
    'font': ('Arial', 10, 'bold'),
    'bg': 'lightblue',
    'fg': 'black',
    'activebackground': 'blue',
    'activeforeground': 'white',
    'width': 15,
    'bd': 3,
    'relief': 'raised'
}

buttons_text = ["Mot de Dyck", "Mot de Motzkin", "Autre"]
buttons_command = [lambda: set_grammar(0), lambda: set_grammar(1), lambda: set_grammar(2)]

for text, command in zip(buttons_text, buttons_command):
    button = tk.Button(btn_frame, text=text, command=command, **button_style)
    button.pack(pady=5)

but_clr = tk.Button(btn_frame, text="Clear", command=clear, font=('Arial', 10, 'bold'), width=15, bg='red', fg='white', bd=3, relief='raised', activebackground='darkred', activeforeground='white')
but_clr.pack(pady=20)

# Frame principale pour les entrées et résultats
main_frame = tk.Frame(root)
main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Label et ScrolledText pour les règles de grammaire
grammar_label = tk.Label(main_frame, text="Entrez les règles de la grammaire:", font=('Arial', 12))
grammar_label.pack(pady=5)
textbox = scrolledtext.ScrolledText(main_frame, height=5, width=80)
textbox.pack(pady=10)

# Label et Entry pour la longueur des mots max
cons_label = tk.Label(main_frame, text="Entrez la longueur des mots max:", font=('Arial', 12))
cons_label.pack(pady=5)
vcmd = (root.register(validate_integer), '%P')
entry = tk.Entry(main_frame, validate='key', validatecommand=vcmd, width=10, font=('Arial', 12))
entry.pack(pady=5)

# Frame pour les contraintes
constraints_frame = tk.Frame(main_frame)
constraints_frame.pack(pady=10)

# Combobox pour sélectionner le terminal
terminal_label = tk.Label(constraints_frame, text="Sélectionner le terminal:", font=('Arial', 12))
terminal_label.grid(row=0, column=0, padx=5)
terminal_combobox = ttk.Combobox(constraints_frame, values=['a', 'b', 'c', 'd'], width=5, font=('Arial', 12))
terminal_combobox.grid(row=0, column=1, padx=5)

# Entry pour entrer la limite
limit_label = tk.Label(constraints_frame, text="Entrer la limite:", font=('Arial', 12))
limit_label.grid(row=1, column=0, padx=5)
limit_entry = tk.Entry(constraints_frame, validate='key', validatecommand=vcmd, width=10, font=('Arial', 12))
limit_entry.grid(row=1, column=1, padx=5)

# Bouton pour ajouter la contrainte
add_button = tk.Button(constraints_frame, text="Ajouter", command=add_constraint, font=('Arial', 10, 'bold'), bg='green', fg='white', bd=3, relief='raised', activebackground='darkgreen', activeforeground='white')
add_button.grid(row=2, column=0, columnspan=2, pady=10)





# Listbox pour afficher les contraintes
constraint_listbox = tk.Listbox(main_frame, width=30, height=5, font=('Arial', 12))
constraint_listbox.pack(pady=10)

# Bouton pour générer les mots
button = tk.Button(main_frame, text="Générer", font=('Arial', 14, 'bold'), command=get_grammar, bg='green', fg='white', bd=3, relief='raised', activebackground='darkgreen', activeforeground='white')
button.pack(pady=20)

# Liste des résultats
Listbox_result = tk.Listbox(main_frame, width=70, height=10, font=('Arial', 12))
Listbox_result.pack(pady=10)

root.mainloop()
