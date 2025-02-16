# Nicolae Marga, FAF-231, Laboratory Work No. 1

import random 

# For type 3 grammars in the Chomsky hierarchy
class Grammar:
    # Constructor for grammar
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
        self.type = self.get_type()
        self.words = []
    
    # Generate all possible strings up to a certain depth
    def generate_string(self, symbol=None, len=0, max_len=100):
        # If no symbol is provided, use the start symbol
        if symbol is None:
            symbol = self.start_symbol

        # It may return the non-terminal symbol to limit the recursion depth
        if len > max_len:
            return symbol

        # Symbol is terminal
        if symbol in self.terminals:
            return symbol

        if symbol in self.productions:
            # Random production
            production = random.choice(self.productions[symbol])
            result = ''
            for sym in production:
                result += self.generate_string(sym, len + 1, max_len)
            return result

        # The symbol doesn't match anything in the production
        raise Exception('Invalid symbol')
    
    # Return a certain number of valid words that is contained in the language 
    def generate_strings(self, num):
        self.words = []
        while len(self.words) < num:
            word = self.generate_string()
            # Only valid and unique words append 
            if all(word[i] in self.terminals for i in range(len(word))) and word not in self.words:
                self.words.append(word)
        return self.words
    # Checks it's type of grammar based on the productions rules
    def get_type(self):
        left_type = False
        right_type = False

        total_rules = []
        for productions_rule in self.productions.values():
            total_rules += productions_rule

        # Get the end result of grammar rules which have length of 2
        rules = [rule for rule in total_rules if len(rule) >= 2]
        print(rules)

        for production in rules:
            # Check if either the non-terminal char is at the right side or the left side
            if all(production[i] in self.terminals for i in range(len(production) - 1)) and production[-1] in self.non_terminals:
                right_type = True
            elif production[0] in self.non_terminals and  all(production[i] in self.terminals for i in range(1, len(production))):
                left_type = True
            else:
                raise ValueError('Invalid type 3 grammar definition')

        if left_type and right_type:
            raise ValueError('The grammar is not of type 3')

        if left_type:
            return 'Left Linear'
        elif right_type:
            return 'Right Linear'
    def to_finite_automaton(self):
        final_state = 'END'
        transitions = {}

        for non_terminal in self.non_terminals:
            transitions[non_terminal] = {}

        for non_terminal, productions in self.productions.items():
            for production in productions:
                if len(production) == 1:  # End terminal production
                    transitions[non_terminal][production] = final_state
                elif self.type == 'Right Linear':
                    transition, new_state = production[:-1], production[1]
                    transitions[non_terminal][transition] = new_state
                elif self.type == 'Left Linear':
                    transition, new_state = production[1], production[:-1]
                    transitions[non_terminal][transition] = new_state
        print(transitions)
        return FiniteAutomaton(
            states=self.non_terminals.union({final_state}),
            alphabet=self.terminals,
            transitions=transitions,
            initial_state=self.start_symbol,
            accept_states=[final_state]
        )
class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
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
    # The method that clasifies the grammar of the object
    print('Classification of grammar: ' + grammar.get_type())
    # The method that generates 5 valid strings
    print('5 random strings from the language expressed by the grammar: ' + str(grammar.generate_strings(5)))
    grammar.to_finite_automaton()