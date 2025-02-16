import random 

# For type 3 grammars in the Chomsky hierarchy
class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
        self.type = self.get_type()
    
    def get_type(self):
        left_type = False
        right_type = False

        total_rules = []
        for productions_rule in self.productions.values():
            total_rules += productions_rule
        print(total_rules)

        # Get the end result of grammar rules which have length of 2
        rules = [rule for rule in total_rules if len(rule) == 2]
        
        for production in rules:
        

            if production[0] in self.terminals and production[1] in self.non_terminals:
                left_type = True
            elif production[0] in self.non_terminals and production[1] in self.terminals:
                right_type = True
            else:
                raise ValueError('Invalid type 3 grammar definition')

        if left_type and right_type:
            raise ValueError('The grammar is not of type 3')

        if left_type:
            return 'Left Linear'
        elif right_type:
            return 'Right Linear'

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