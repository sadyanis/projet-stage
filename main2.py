import tkinter as tk
from tkinter import scrolledtext, messagebox
#from deque import *
from version_cons import *
import itertools
import sys
from collections import deque
from nltk.grammar import CFG, Nonterminal
from tkinter import ttk
from grammar import grammar_list
from tkinter import filedialog, messagebox
constraints = {}
Values = []


# Fonction qui detecte tous les terminaux
def get_terminals():
    grammar = CFG.fromstring(textbox.get("1.0", tk.END).strip())
    terminals = set()
    for production in grammar.productions():
        for symbol in production.rhs():
            if isinstance(symbol, str):
                terminals.add(symbol)
    
    return list(terminals)

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
    
    grammar = CFG.fromstring(grammar_text)
    words = list(generate_iterative(grammar, max_length=const, max_constraints=constraints))
    Listbox_result.delete(0, tk.END)
    for n, sent in enumerate(words, 1):
        Listbox_result.insert(tk.END, f"{n:3d}. {sent}")

# Définit la grammaire usuelle
def set_grammar(index):
    textbox.delete("1.0", tk.END)
    textbox.insert(tk.END, grammar_list[index].strip())

# Efface le texte du textbox
def clear():
    textbox.delete("1.0", tk.END)
    constraint_listbox.delete(0,tk.END)
    constraints = {}


# Met à jour la Combobox avec les terminaux extraits de la grammaire
def update_combo(event=None):
    grammar_text = textbox.get("1.0", tk.END).strip()
    terminals = get_terminals()
    terminal_combobox['values'] = terminals    

# Ajoute une contrainte à la liste des contraintes
def add_constraint():
    terminal = terminal_combobox.get()
    limit = limit_entry.get()
    if terminal and limit:
        constraint_listbox.insert(tk.END, f"{terminal}: {limit}")
        constraints[terminal] = int(limit)
        terminal_combobox.set('')
        limit_entry.delete(0, tk.END)
        print(constraints)
    else:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un terminal et entrer une limite.")
# charger une grammar depuis un fichier        
def load_grammar():
    file_path = filedialog.askopenfilename(
        title="Sélectionnez un fichier de grammaire",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                grammar_content = file.read()
                    # Optionally parse the grammar to ensure it's valid
                grammar = CFG.fromstring(grammar_content)  # Ensure valid CFG
                textbox.delete(1.0, tk.END)
                textbox.insert(tk.END, grammar_content)
                messagebox.showinfo("Succès", "Grammaire chargée avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger la grammaire : {str(e)}")

def get_words_from_listbox():
        words = Listbox_result.get(0, tk.END)
        return words

def save_grammar():
    words = get_words_from_listbox()
    if not words:
        messagebox.showerror("Erreur", "Aucun mot généré à sauvegarder.")
        return
    
    file_path = filedialog.asksaveasfilename(
            title="Sauvegarder les mots générés",
            defaultextension=".txt",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
    if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    for word in words:
                        file.write(word + '\n')
                messagebox.showinfo("Succès", "Mots sauvegardés avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder les mots : {str(e)}")


    
# Création de la fenêtre principale
root = tk.Tk()
root.geometry("1000x1000")
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
textbox.bind("<KeyRelease>",update_combo)

constraint_frame = tk.Frame(main_frame)
constraint_frame.pack(padx=5,pady=5, fill=tk.BOTH,expand=True)

# Label et Entry pour la longueur des mots max
cons_label = tk.Label(constraint_frame, text="Entrez la longueur des mots max:", font=('Arial', 12))
cons_label.grid(row=1,column=2, pady=5)
vcmd = (root.register(validate_integer), '%P')
entry = tk.Entry(constraint_frame, validate='key', validatecommand=vcmd, width=10, font=('Arial', 12))
entry.grid(row=1,column=3,pady=5)



terminal_label = tk.Label(constraint_frame, text="Sélectionner le terminal:", font=('Arial', 12))
terminal_label.grid(row=0, column=0, padx=5)
terminal_combobox = ttk.Combobox(constraint_frame, width=8, font=('Arial', 12))
terminal_combobox.bind("<Button-1>", get_terminals)
terminal_combobox.grid(row=0, column=1, padx=5)

btn_load = tk.Button(constraint_frame, text="Charger Grammaire", command=load_grammar, font=('Arial', 10, 'bold'), width=15, bg='grey', fg='white', bd=3, relief='raised', activebackground='darkred', activeforeground='white')
btn_load.grid(row=0,column=3)

# Entry pour entrer la limite
limit_label = tk.Label(constraint_frame, text="Entrer la limite:", font=('Arial', 12))
limit_label.grid(row=1, column=0, padx=5)
limit_entry = tk.Entry(constraint_frame, validate='key', validatecommand=vcmd, width=10, font=('Arial', 12))
limit_entry.grid(row=1, column=1, padx=5)

# button d'ajout
add_button = tk.Button(constraint_frame, text="Ajouter",command=add_constraint,width=10, font=('Arial', 10, 'bold'), bg='green', fg='white', bd=3, relief='raised', activebackground='darkgreen', activeforeground='white')
add_button.grid(row=2,column=1,columnspan=2, pady=10)


#Affichage des contraintes

constraint_listbox = tk.Listbox(main_frame, width=30, height=3, font=('Arial', 12))
constraint_listbox.pack(pady=1)


# Bouton pour générer les mots
button = tk.Button(main_frame, text="Générer", font=('Arial', 14, 'bold'), command=get_grammar, bg='green', fg='white', bd=3, relief='raised', activebackground='darkgreen', activeforeground='white')
button.pack(pady=20)


result_frame = tk.Frame(root)
result_frame.pack(pady=10)

Listbox_result = tk.Listbox(result_frame, width=60, height=10, font=('Arial', 12))
Listbox_result.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(result_frame, text="Sauvegarder", font=('Arial', 14, 'bold'), command=save_grammar, bg='blue', fg='white', bd=3, relief='raised', activebackground='darkgreen', activeforeground='white')
save_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
