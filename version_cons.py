import sys
from collections import deque
from nltk.grammar import CFG, Nonterminal

def generate_iterative(grammar, start=None, max_length=8, max_constraints=None):
    """
    Génère un itérateur de toutes les phrases à partir d'une grammaire hors-contexte (CFG) en utilisant une approche itérative
    avec des contraintes sur le nombre maximal de symboles terminaux.

    :param grammar: La grammaire utilisée pour générer les phrases.
    :param start: Le symbole non terminal à partir duquel commencer la génération des phrases.
    :param max_length: La longueur maximale des phrases générées.
    :param max_constraints: Un dictionnaire avec les terminaux comme clés et leurs contraintes maximales respectives comme valeurs.
    :return: Un itérateur de listes de tokens terminaux.
    """

    if not start:
        start = grammar.start()

    if max_constraints is None:
        max_constraints = {}

    queue = deque([([start], '', {term: 0 for term in max_constraints})])  # ( éléments à développer, séquence générée, nombre de terminaux)

    while queue:
        current_items, generated, terminal_count = queue.popleft()
        if not current_items:
            if len(generated) <= max_length:
                yield generated
            continue

        item, rest = current_items[0], current_items[1:]
        if isinstance(item, Nonterminal):
            for production in grammar.productions(lhs=item):
                new_items = list(production.rhs()) + rest
                queue.append((new_items, generated, terminal_count.copy()))
        else:
            new_generated = generated + item
            new_terminal_count = terminal_count.copy()
            if item in max_constraints:
                new_terminal_count[item] += 1
                if new_terminal_count[item] > max_constraints[item]:
                    continue
            if len(new_generated) <= max_length:
                queue.append((rest, new_generated, new_terminal_count))

def demo_iterative(grammar_text, max_length=8, max_constraints=None):
    grammar = CFG.fromstring(grammar_text)
    
   
    print(grammar_text)
    
    words = list(generate_iterative(grammar, max_length=max_length, max_constraints=max_constraints))
    for n, sent in enumerate(words, 1):
        print(f"{n:3d}. {sent}")

if __name__ == "__main__":
    # Exemple de grammaire fournie par l'utilisateur
    grammar_text = """
      S -> 'a' 't' 'b'  | 'a' 't' 'b' S | 'a' S 'b' | 'a' S 'b' S
    """
    
    # Contraintes maximales sur les terminaux fournies par l'utilisateur
    max_constraints = {
        'a': 4,  # Au plus 4 'a'
        't': 2   # Au plus 2 'b'
        # Ajoutez d'autres terminaux avec leurs contraintes maximales si nécessaire
        # Si un terminal n'a pas de contraintes maximales, ne l'ajoutez pas au dictionnaire
    }
    
    demo_iterative(grammar_text, max_length=20, max_constraints=max_constraints)
