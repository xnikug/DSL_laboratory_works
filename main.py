from graphviz import Digraph, Source
import random 
class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
        

if __name__ == "__main__":
    grammar = Grammar(
        non_terminals={"S", "B", "C", "D"},
        terminals={"a", "b", "c"},
        productions={
            "S": ["aB"],
            "B": ["bS", "aC", "b"],
            "C": ["bD"],
            "D": ["a", "bC", "cS"]
        },
        start_symbol="S"
    )
    pass