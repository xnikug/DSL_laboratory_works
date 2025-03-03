from graphviz import Digraph, Source
import random
# Nicolae Marga, FAF-231, Laboratory Work No. 2
'''
Variant 21
Q = {q0,q1,q2,q3},
∑ = {a,b,c},
F = {q3},
δ(q0,a) = q0,
δ(q0,a) = q1,
δ(q1,b) = q2,
δ(q2,c) = q3,
δ(q3,c) = q3,
δ(q2,a) = q2.
'''
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
        #print(rules)

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
    def to_finite_automaton(self, final_states = None):
        final_state = 'dead'
        transitions = {}
        for non_terminal in self.non_terminals:
            transitions[non_terminal] = {}
        for non_terminal, productions in self.productions.items():
            for production in productions:
                if len(production) == 1:  # End terminal production
                    transitions[non_terminal][production] = final_state
                elif self.type == 'Right Linear':
                    transition, new_state = production[:-1], production[1]
                    if non_terminal in transitions and transition in transitions[non_terminal]:
                         transitions[non_terminal][transition].append(new_state)
                    else:
                        transitions[non_terminal][transition] = [new_state]
                    
                elif self.type == 'Left Linear':
                    transition, new_state = production[1], production[:-1]
                    if non_terminal in transitions and transition in transitions[non_terminal]:
                         transitions[non_terminal][transition].append(new_state)
                    else:
                        transitions[non_terminal][transition] = [new_state]
        print("Conversion to transitions: " + str(transitions))
        if final_states == None:
            final_states = {final_state}
        return FiniteAutomaton(
            states=self.non_terminals.union(final_states),
            alphabet=self.terminals,
            start_state=self.start_symbol,
            final_states=final_states,
            transitions=transitions
        )
class FiniteAutomaton:
    def __init__(self, states, alphabet, start_state, final_states, transitions):
        self.states = states  # Set of states
        self.alphabet = alphabet  # Alphabet (input symbols)
        self.start_state = start_state  # Start state
        self.final_states = final_states  # Set of final states
        self.transitions = transitions  # Transition function (dict of dicts)
        self.is_dfa = self.is_deterministic()

    def is_deterministic(self):
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                if len(next_states) > 1:
                    return False
        return True
    def create_diagram(self):
        dot = Digraph(comment='Finite Automaton')
        dot.attr(rankdir='LR')

        # Add states
        for state in self.states:
            dot.node(state, state, shape='doublecircle' if state in self.final_states else 'circle')

        # Mark initial state
        dot.node('', '', shape='none')
        dot.edge('', self.start_state)

        # Add transitions
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    dot.edge(state, next_state, label=symbol)

        return dot
    def to_regular_grammar(self):
        non_terminals = self.states 
        terminals = self.alphabet
        start_symbol = self.start_state
        rules = {nt: [] for nt in non_terminals}

        # Transform transitions into production rules
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    rules[state].append(f"{symbol}{next_state}")
                    # If the next state is an accept state, add a production rule ending in the terminal
                    if next_state in self.final_states and not self.transitions.get(next_state):
                        rules[state].append(symbol)

        return Grammar(non_terminals, terminals, rules, start_symbol)    
    def to_dfa(self):
        if self.is_deterministic():
            return self
        init_s = self.start_state
        dfa_transitions = {}
        dfa_accept_states = []
        queue = [frozenset([init_s])]
        visited = set()
        dfa_states_map = {frozenset([init_s]): init_s}

        while queue:
            current_states = queue.pop(0)
            if current_states in visited:
                continue
        
            visited.add(current_states)

            if len(current_states) == 1:
                dfa_state_name = next(iter(current_states))
            else:
                dfa_state_name = ', '.join(sorted(current_states))
            dfa_transitions[dfa_state_name] = {}

            for symbol in self.alphabet:
                # Get the set of states for a given symbol
                next_states_set = set()  # Use a set to store unique next states

                for state in current_states:
                    # Get the dictionary of transitions for the current state
                    state_transitions = self.transitions.get(state, {})
                    next_states = state_transitions.get(symbol, [])
                    # Add the next states to the set
                    next_states_set.update(next_states)
                # Convert to frozenset to maintain immutability
                next_states_set = frozenset(next_states_set)

                if not next_states_set:
                    continue

                if len(next_states_set) == 1:
                    next_state_name = next(iter(next_states_set))
                else:
                    next_state_name = ', '.join(sorted(next_states_set))

                dfa_transitions[dfa_state_name][symbol] = [next_state_name]  

                if next_states_set not in dfa_states_map:
                    dfa_states_map[next_states_set] = next_state_name
                    queue.append(next_states_set)
                # If the newly formed state set intersects with an existing final state
                # Then set the new state as final
                if next_states_set.intersection(self.final_states):
                    dfa_accept_states.append(next_state_name)

        dfa_states = list(dfa_states_map.values())
        print(dfa_states)
        return FiniteAutomaton(
            states=dfa_states,
            alphabet=self.alphabet,
            transitions=dfa_transitions,
            start_state=dfa_states_map[frozenset([self.start_state])],
            final_states=dfa_accept_states
        )
    def _state_set_to_name(self, states_set):
        # Return the existing state name if it's a single state
        if len(states_set) == 1:
            return next(iter(states_set))

        # Create a composite state name by joining state names with ,
        return ','.join(sorted(states_set))
            
if __name__ == '__main__':
    # FA definition based on provided details
    Q = {'0', '1', '2', '3'}
    Σ = {'a', 'b', 'c'}
    F = {'3'}
    start_state = '0'
    transitions = {
        '0': {'a': ['0', '1']},
        '1': {'b': ['2']},
        '2': {'c': ['3'], 'a': ['2']},
        '3': {'c': ['3']},
    }
    print("Original defined transitions: " + str(transitions))
    # Create the finite automaton
    fa = FiniteAutomaton(Q, Σ, start_state, F, transitions)

    # Check if the automaton is deterministic
    print("Is the automaton deterministic?", fa.is_deterministic())

    # Conversion from fa to grammar
    grammar = fa.to_regular_grammar()
    print("The Converted Grammar G = {V_N, V_T, S, V_P}")
    print("V_N = " + str(grammar.non_terminals))
    print("V_T = " + str(grammar.terminals))
    print("S = " + str(grammar.start_symbol))
    print("V_P = " + str(grammar.productions))
    
    # Conversion from grammar back to fa
    fa = grammar.to_finite_automaton(F)
    fa.create_diagram().render('ndfa', format='png')

    dfa = fa.to_dfa()
    dfa.create_diagram().render('dfa', format='png')


    