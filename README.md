# Laboratory Work No. 5
### Course: Formal Languages & Finite Automata  
### Author: Nicolae Marga
### Group: FAF-231

----
## Theory

**Parsing** is the process of analyzing text according to the rules of a formal grammar. It typically follows lexical analysis (tokenization) and constructs a structured representation of the input text. Parsing involves determining the syntactic structure of the input and validating that it conforms to the expected grammar.

An **Abstract Syntax Tree (AST)** is a hierarchical tree representation of the abstract syntactic structure of source code. Each node in the tree represents a construct in the source code. The AST abstracts away details like parentheses, semicolons, or other syntactic sugar, focusing on the essential structure and meaning of the code.

### Parsing Process

The parsing process typically consists of two main phases. Breaking the input text into tokens, and organizing the tokens into a hierarchical structure. Parsing errors occur when tokens cannot be organized according to the grammar rules, even if individual tokens are valid.


## Objectives
1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens. 
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.


## Implementation Description

### TokenType Enum

The `TokenType` enum was implemented using Python's `Enum` class with `auto()` to assign automatically values. This enum classifies tokens into categories like keywords (SELECT, FROM, WHERE), operators (=, >, <), and literals (identifiers, numbers, strings).

### AST Node Classes

There is a set hierarchy of classes in order to represent different elements of SQL queries in the AST:

- `ASTNode`: Base class for all AST nodes
- `SelectStatement`: Represents a complete SELECT statement
- `CreateProcedureStatement`: Represents a CREATE PROCEDURE statement
- `ColumnReference`: Represents a reference to a column
- `WhereClause`: Represents a WHERE clause with conditions
- `BinaryOperation`: Represents comparison operations (e.g., column = value)
- `LogicalOperation`: Represents logical operations (AND, OR)
- `Literal`: Represents literal values (numbers, strings)
- `Parameter`: Represents parameters in stored procedures

### Parser Implementation

The parser takes a recursive descent approach to processes tokens sequentially and builds an AST. It examines the first token to determine the statement type. It calls specialized methods to parse different parts of the statement, and creates appropriate AST nodes to represent the structure. The parser also handles errors when the input doesn't match the expected grammar.

### Error Handling

There are two types of error handling:

- `LexerError`: For issues with individual tokens or unrecognized characters
- `ParserError`: For issues with the syntactic structure of the query

### AST Visualization

A function was created in order to visualize the AST as a tree structure using ASCII characters, which makes it easier to understand the hierarchical relationships between tokens in the query.

## Results

-



## Conclusions

-

## References:
[1] [Parsing Wiki](https://en.wikipedia.org/wiki/Parsing)

[2] [Abstract Syntax Tree Wiki](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
