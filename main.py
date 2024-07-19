import tkinter as tk
from tkinter import scrolledtext, messagebox
from deque import *
import itertools
import sys
from collections import deque
from nltk.grammar import CFG, Nonterminal
from grammar import grammar_list
def validate_integer(P):
    """
    Cette fonction vérifie si la chaîne P est un entier.
    P : chaîne de caractères entrée par l'utilisateur
    Retourne : True si P est un entier ou vide, False sinon
    """
    if P.isdigit() or P == "":
        return True
    else:
        return False
    


# fonction qui verifie si un champ est vide
def is_empty():
    if  len( textbox.get("1.0",tk.END).strip())==0 or  len(entry.get())==0:
         messagebox.showwarning("Erreur", "Veuillez renseigner tous les champs.")
         return True    
    return False
# fonction qui recupere la grammaire depuis le textbox
def get_grammar():
    if is_empty():
        return
    grammar_text = textbox.get("1.0",tk.END).strip()
    const = int(entry.get())
    grammar = CFG.fromstring(grammar_text)
    

    print(f"Generating sentences of length <= 8 for the given grammar:")
    print(grammar)
    
    words = list(generate_iterative(grammar, max_length=const))
    for n, sent in enumerate(words, 1):
        Listbox_result.insert(tk.END,f"{n:3d}. {sent}")

#fonction des button de grammaire usuelle:
def set_grammar():
    textbox.delete("1.0",tk.END)
    textbox.insert(tk.END,grammar_list[0].strip())     

#fonction pour 
def clear():
    textbox.delete("1.0",tk.END)

#comment
def set_grammar2():
    textbox.delete("1.0",tk.END)
    textbox.insert(tk.END,grammar_list[1].strip()) 

# comment 2

def set_grammar3():
    textbox.delete("1.0",tk.END)
    textbox.insert(tk.END,grammar_list[2].strip())     

#dasda
def set_grammar4():
    textbox.delete("1.0",tk.END)
    textbox.insert(tk.END,grammar_list[3].strip()) 
#creation d'une fenetre simple

root = tk.Tk() # la racine de l'interface graphique
root.geometry("800x500")#ajuster les dimension de la fenetre
root.title("Grammar generator")

label = tk.Label(root, text ="Welcom to Grammar generator", font = ('Arial',18,'italic'))#creer un Label
label.pack(padx=20, pady=20)

btn_frame = tk.Frame(root,height=100)
btn_frame.pack(side=tk.RIGHT,anchor='n', padx=10,pady=10 )

label_ram = tk.Label(btn_frame,text="Grammaires usuelle:", font=('Arial',10) )
label_ram.pack(padx=10)

grammar_label = tk.Label(root, text="Entrez les regles de la grammaire:" ,font=('Arial',12))
grammar_label.pack(padx=20)

button1 = tk.Button(btn_frame, text="Mot de dyck", command=set_grammar)
button1.pack(fill=tk.X, pady=10)  # fill=tk.X pour que les boutons s'étendent horizontalement

button2 = tk.Button(btn_frame, text="mot de motzkin" ,command=set_grammar2)
button2.pack(fill=tk.X, pady=10)

button3 = tk.Button(btn_frame, text="autre")
button3.pack(fill=tk.X, pady=10)

but_clr = tk.Button(btn_frame, text="Clear", command=clear)
but_clr.pack(fill=tk.X, pady=10)




textbox = scrolledtext.ScrolledText(root, height=3,width=60)
textbox.pack()

cons_label = tk.Label(root, text="Entrez la longeur des mots max " ,font=('Arial',12))
cons_label.pack(padx=20)

# Configuration de la validation
vcmd = (root.register(validate_integer), '%P')

entry = tk.Entry(root,validate='key', validatecommand=vcmd )
entry.pack()

button = tk.Button(root, text="Generer", font=('Arial',16),command=get_grammar)
button.pack(padx=12,pady=15)

Listbox_result = tk.Listbox(root, width=70,height=10)
Listbox_result.pack()
root.mainloop()#responsable de l'affichage

