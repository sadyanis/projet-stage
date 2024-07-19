from nltk.grammar import CFG, Nonterminal
dyck = """
      S -> 'a' 't' 'b'  | 'a' 't' 'b' S | 'a' S 'b' | 'a' S 'b' S
    """
g2 = """
      S -> 'a' S 'b'  | ''
    """
g3 = """
      S -> 'a' S  | 'b' S | '' 
    """
g4 = """
      S -> 'a' S 'b' 'b'  | 'c' 
    """

grammar_list = [dyck  ,g2, g3 , g4 ]
