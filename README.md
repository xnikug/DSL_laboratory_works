# Nicolae Marga, FAF-231, Laboratory Work No. 1

### Course: Formal Languages & Finite Automata  
### Author: Nicolae Marga

----

## Theory

This work focuses on Type 3 grammars in the Chomsky hierarchy, which are regular grammars used to define regular languages. The main objective is to create a class that represents these grammars, generate valid strings, classify the grammar, and convert it into a finite automaton. The finite automaton simulates the state transitions that accept or reject input strings.

## Objectives:

* Implement a class that defines Type 3 grammars and generates valid strings.
* Classify the grammar as left-linear or right-linear based on production rules.
* Convert the grammar into a finite automaton.
* Check whether a given input string is accepted by the finite automaton.

## Implementation description

The program consists of two main classes: `Grammar` and `FiniteAutomaton`.

* The **Grammar** class defines the grammar's non-terminals, terminals, and production rules. It can generate valid strings, classify the grammar, and convert it into a finite automaton.
* The **FiniteAutomaton** class takes the grammar's production rules and creates an automaton that can check if a string is accepted by the grammar.

### Conclusions / Results
This laboratory work how to convert a Type 3 grammar into a finite automaton and check if input strings can be accepted by it. The implementation includes functions for generating strings, classifying grammar types, and simulating state transitions in a finite automaton.
