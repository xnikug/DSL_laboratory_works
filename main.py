from graphviz import Digraph, Source
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

if __name__ == '__main__':
    # FA definition based on provided details
    Q = {"q0", "q1", "q2", "q3"}
    Σ = {"a", "b", "c"}
    F = {"q3"}
    start_state = "q0"
    transitions = {
        "q0": {"a": ["q0", "q1"]},
        "q1": {"b": ["q2"]},
        "q2": {"c": ["q3"], "a": ["q2"]},
        "q3": {"c": ["q3"]},
    }

    # Create the finite automaton
    fa = FiniteAutomaton(Q, Σ, start_state, F, transitions)

    # Check if the automaton is deterministic
    print("Is the automaton deterministic?", fa.is_deterministic())
    fa.create_diagram().render('finite_automaton', format='png')