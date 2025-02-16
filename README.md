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


## Results
- In the output the classification of the grammar is present, also there are 5 strings generated from the grammar.
- It is shown the state transitions of the finite automaton
- Some checks are performed for 4 strings
```python
    print(finite_automaton.check("ab"))
    print(finite_automaton.check("aaba"))
    print(finite_automaton.check("aabcab"))
    print(finite_automaton.check("aa"))
```
![The final output of the program](image-1.png)
## Conclusions
This laboratory work demonstrates how to convert a Type 3 grammar into a finite automaton and check if input strings can be accepted by it. The implementation includes functions for generating strings, classifying grammar types, and simulating state transitions in a finite automaton.