""" 
import nltk
from nltk.grammar import CFG
from collections import deque

# Définir la grammaire context-free (CFG)
grammar = CFG.fromstring(
    S -> 'a' S 'b' | 'c'
)

def generate_words_bfs(grammar, max_length):
    
    
    words = set()
    queue = deque([('S', '')])  # Une file d'attente pour BFS, commençant avec le symbole de départ

    while queue:
        current, generated_word = queue.popleft()

        # Si le mot généré est de longueur <= max_length, l'ajouter aux résultats
        if len(generated_word) <= max_length:
            if all(char.islower() for char in generated_word):  # Assurez-vous que c'est un mot complet
                words.add(generated_word)
        
        # Si la longueur actuelle est inférieure à max_length, continuer à générer
        if len(generated_word) < max_length:
            for production in grammar.productions(lhs=nltk.Nonterminal(current)):
                new_word = generated_word + ''.join(prod.symbol() if isinstance(prod, nltk.Terminal) else '' for prod in production.rhs())
                if len(new_word) <= max_length:
                    queue.append((str(production.rhs()), new_word))
    
    return words

# Spécifier la longueur maximale n
max_length = 8

# Générer les mots
words = generate_words_bfs(grammar, max_length)

# Afficher les mots générés
for word in sorted(words):
    print(word)
"""
import itertools
import sys
from collections import deque
from nltk.grammar import CFG, Nonterminal


def get_grammar_from_user():
    print("Veuiller entrer votre grammaire (terminer par une ligne vide)")
    grammar_rule = []
    while True:
        line = input()
        if not line.strip():
            break
        grammar_rule.append(line)
    grammar_text = "\n".join(grammar_rule)
    grammar = CFG.fromstring(grammar_text)
    return grammar

def generate_iterative(grammar, start=None, max_length=8):
    """
    Generates an iterator of all sentences from a CFG using an iterative approach.

    :param grammar: The Grammar used to generate sentences.
    :param start: The Nonterminal from which to start generating sentences.
    :param max_length: The maximum length of the generated sentences.
    :return: An iterator of lists of terminal tokens.
    """
    if not start:
        start = grammar.start()

    queue = deque([([start], '')])  # (items to expand, generated sequence)

    while queue:
        current_items, generated = queue.popleft()
        if not current_items:
            if len(generated) <= max_length:
                yield generated
            continue

        item, rest = current_items[0], current_items[1:]
        if isinstance(item, Nonterminal):
            for production in grammar.productions(lhs=item):
                new_items = list(production.rhs()) + rest
                queue.append((new_items, generated))
        else:
            new_generated = generated + item
            if len(new_generated) <= max_length:
                queue.append((rest, new_generated))

def demo_iterative(grammar,max_length=8):
    from nltk.grammar import CFG

    # grammar_text = """
    #   S -> 'a' S | ''
    # """
    # grammar = CFG.fromstring(grammar_text)
    
    print(f"Generating sentences of length <= {max_length} for the given grammar:")
    print(grammar)
    
    words = list(generate_iterative(grammar, max_length=max_length))
    for n, sent in enumerate(words, 1):
        print(f"{n:3d}. {sent}")

if __name__ == "__main__":
    grammar = get_grammar_from_user()
    taille_mot = int(input("\nQuelle est la longueur maximale des mots/phrases que vous voulez générer ? "))
    demo_iterative(grammar,max_length=taille_mot)


