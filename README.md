# Laboratory Work No. 1

### Course: Formal Languages & Finite Automata  
### Author: Nicolae Marga
### Group: FAF-231

----

## Theory
This work focuses on Type 3 grammars in the Chomsky hierarchy, which are regular grammars used to define regular languages. The main objective is to create a class that represents these grammars, generate valid strings, classify the grammar, and convert it into a finite automaton. The finite automaton simulates the state transitions that accept or reject input strings.

## Objectives:
* Implement a class that defines Type 3 grammars and generates valid strings
* Classify the grammar as left-linear or right-linear based on production rules
* Convert the grammar into a finite automaton 
* Check whether a given input string is accepted by the finite automaton
* The given grammar is the following:
```python
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
```
## Implementation description

The program consists of two main classes: `Grammar` and `FiniteAutomaton`.

### Grammar Class Methods:

#### __init__(self, non_terminals, terminals, productions, start_symbol)
Constructor that initializes a grammar with:
- Set of non-terminal symbols
- Set of terminal symbols  
- Production rules (as a dictionary)
- Starting symbol
- Automatically determines the grammar type (left/right linear)

#### generate_string(self, symbol=None, len=0, max_len=100)
- Recursively generates a single valid string from the grammar
- Uses random production rules to create the string
- Has a max length parameter to prevent infinite recursion
- Returns a string of terminal symbols
```py
def generate_string(self, symbol=None, len=0, max_len=100):
    if symbol is None:
        symbol = self.start_symbol
    if len > max_len:
        return symbol
    if symbol in self.terminals:
        return symbol
    if symbol in self.productions:
        production = random.choice(self.productions[symbol])
        result = ''
        for sym in production:
            result += self.generate_string(sym, len + 1, max_len)
        return result
```
#### generate_strings(self, num)
- Generates multiple unique valid strings from the grammar
- Takes a number parameter for how many strings to generate
- Uses generate_string() internally and ensures uniqueness 
- Returns a list of valid strings

#### get_type(self)
- Determines if the grammar is left-linear or right-linear
- Analyzes production rules to check their structure:
 - Left-linear: Non-terminal appears at start
 - Right-linear: Non-terminal appears at end
- Throws an error if grammar isn't Type 3
```py
def get_type(self):
    left_type = False
    right_type = False
    
    total_rules = []
    for productions_rule in self.productions.values():
        total_rules += productions_rule

    rules = [rule for rule in total_rules if len(rule) >= 2]

    for production in rules:
        if all(production[i] in self.terminals for i in range(len(production) - 1)) \
           and production[-1] in self.non_terminals:
            right_type = True
        elif production[0] in self.non_terminals and \
             all(production[i] in self.terminals for i in range(1, len(production))):
            left_type = True
        else:
            raise ValueError('Invalid type 3 grammar definition')
            
    return 'Left Linear' if left_type else 'Right Linear'
```
#### to_finite_automaton(self)
- Converts the grammar to an equivalent finite automaton
- Creates states from non-terminals
- Transforms production rules into transition functions 
- Returns a new FiniteAutomaton object

### FiniteAutomaton Class Methods:

#### __init__(self, states, alphabet, transitions, initial_state, accept_states)
Constructor that initializes an automaton with:
- Set of states
- Input alphabet
- Transition functions  
- Initial state
- Set of accepting states

#### check(self, input_string)
- Verifies if an input string is accepted by the automaton
- Simulates the automaton by following state transitions
- Returns True if string reaches an accepting state, False otherwise
```py
def check(self, input_string):
    curr_state = self.initial_state
    for symbol in input_string:
        # Check for valid symbols
        if symbol not in self.alphabet:
            return False 
        # Check for transitions
        if curr_state in self.transitions and symbol in self.transitions[curr_state]:
            curr_state = self.transitions[curr_state][symbol]
        else:
            return False
    return curr_state in self.accept_states
```

## Results
- In the output the classification of the grammar is present, also there are 5 strings generated from the grammar.
- It is shown the state transitions of the finite automaton
- Some checks are performed for 4 strings, example in the code are the following:
```python
    print(finite_automaton.check("ab"))
    print(finite_automaton.check("aaba"))
    print(finite_automaton.check("aabcab"))
    print(finite_automaton.check("aa"))
```
- The final output of the program
![The final output of the program](image-1.png)
## Conclusions
This laboratory work demonstrates how to convert a Type 3 grammar into a finite automaton and check if input strings can be accepted by it. The implementation includes functions for generating strings, classifying grammar types, and simulating state transitions in a finite automaton.