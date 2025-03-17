# Laboratory Work No. 3

### Course: Formal Languages & Finite Automata  
### Author: Nicolae Marga
### Group: FAF-231

----
## Theory
Lexical analysis serves as the first phase in compiler and interpreter design, functioning as the bridge between raw text and structured data. This process transforms an unstructured sequence of characters into a stream of meaningful tokens that subsequent compilation phases can process. The fundamental operations begin with scanning, where the lexer reads through the input characters one at a time, identifying patterns and boundaries within the text. As it scans, the lexer performs recognition by isolating lexemes sequences of characters that form logical units within the language, such as keywords, identifiers, or literals.

Once lexemes are identified, the classification stage assigns each lexeme to a specific token type based on the language's rules and grammar. This categorization is important for determining how each element should be treated during parsing and semantic analysis. The final stage, token generation, produces the actual token objects that contain both the token type (such as "keyword," "identifier," or "operator") and the actual value encountered in the source code. These tokens serve as the fundamental building blocks that will be assembled into syntactic structures during parsing.

In programming language processing, lexical analysis deliberately operates at a surface level, concerned exclusively with the structural composition of individual words and symbols without attempting to understand their contextual meaning or relationships. This separation of concerns allows the lexer to focus solely on recognizing valid language elements like keywords, identifiers, literals (strings or numbers), operators (arithmetic or comparison symbols), and punctuation. By maintaining this narrow focus, the lexer creates a tokenized representation of the source code that simplifies the complex tasks of syntactic and semantic analysis.

## Objectives:

1. Design and implement a lexer:
   - Understand what lexical analysis is.
   - Get familiar with the inner workings of a lexer/scanner/tokenizer.
   - Implement a sample lexer and show how it works.

## Implementation description
The implementation consists of a SQL query lexer designed to transform raw SQL text into structured tokens for further processing. The Python's regular expression capabilities are used, this lexer handles common SQL syntax including SELECT statements, WHERE clauses, and stored procedure definitions.

### Token Definition

The lexer begins by defining the token types it needs to recognize using regular expressions:

```python
TOKENS = {
    'SELECT': r'\bSELECT\b',
    'FROM': r'\bFROM\b',
    'WHERE': r'\bWHERE\b',
    'AND': r'\bAND\b',
    'OR': r'\bOR\b',
    'EQUALS': r'=',
    'GREATER': r'>',
    'LESS': r'<',
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*|\*',
    'NUMBER': r'-?\d+(\.\d+)?',
    'STRING': r'\'[^\']*\'',
    'COMMA': r',',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'WHITESPACE': r'\s+',
    'CREATE': r'\bCREATE\b',
    'PROCEDURE': r'\bPROCEDURE\b',
    'PARAMETER': r'@[a-zA-Z_][a-zA-Z0-9_]*',
}
```

These patterns are combined into a master regex that matches all possible tokens:

```python
MASTER_REGEX = '|'.join(f'(?P<{key}>{value})' for key, value in TOKENS.items())
```

The named capture groups allow the lexer to identify which token type was matched.

### Core Lexer Implementation

The `QueryLexer` class encapsulates the lexical analysis process:

The tokenization process handles input by iterating through all regex matches in the query string. Throughout this traversal, it conducts thorough checks for any unrecognized characters that might appear between valid matches, raising errors with position information when detected. As tokens are identified, the process determines their types based on which named capture group was matched in the regular expression, which provides classification for each element. The implementation manages special cases, skipping whitespace tokens while processing string literals by removing surrounding quotes to extract their content values. Finally, it builds a list of tokens which are represented as (type, value) pairs, creating a more structured output that's ready for subsequent parsing stages.
### Error Handling

A custom exception class provides detailed error information:

```python
class LexerError(Exception):
    """Exception raised for errors during lexical analysis."""
    def __init__(self, message, position):
        self.message = message
        self.position = position
        super().__init__(f"{message} at position {position}")
```

The lexer can detect and report:
- Empty input
- Unrecognized characters
- Malformed string literals

A helper function provides error reporting:

```python
def tokenize_query(query):
    """Wrapper function to handle lexer errors gracefully"""
    try:
        lexer = QueryLexer(query)
        return lexer.tokenize()
    except LexerError as e:
        print(f"Lexer Error: {e}")
        # Show the position with a caret
        if query:
            print(query)
            print(' ' * e.position + '^')
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

This function not only catches and displays errors but also visually indicates their location in the input.

### Testing

The implementation includes sample queries to test both successful tokenization and error cases:

```python
queries = [
    queries = [
        "SELECT name, age FROM users WHERE age > 21 AND city = 'New York'",  # Valid
        "SELECT *$* FROM users",  # Invalid character
        "SELECT name, $ge FROM users",  # Invalid character
        "SELECT name, age FROM users WHERE age > 18 AND city = 'Washington",  # Unclosed string
        "SELECT 123.name FROM users",  # Invalid identifier starting with number
        "$%^&",  # Invalid characters
        "",  # Empty query
        "SELECT name, age FROM users WHERE age > 18 AND city = 'New'York' ",  # Unmatched quotes
        "CREATE PROCEDURE myProc(@param1 INT, @param2 VARCHAR(100)) AS BEGIN SELECT * FROM users END"  # Stored procedure creation
        "CREATE PROCEDURE invalidProc(param1 IN%, @param2 VARCHAR(100)) AS BEGIN SELECT * FROM users END"  # Invalid parameters definition
    ]
]
```
In Query 1 it is shown the tokenization of a valid SQL query, where each part of "SELECT name, age FROM users WHERE age > 21 AND city = 'New York'" has been identified and categorized into tokens like SELECT, IDENTIFIER, COMMA, GREATER, etc.

![Valid query syntax](image.png)

Next, in Query 2, the lexer caught the invalid wildcard character "\$*\$" as an unrecognized token at position 8. Query 3 shows detection of the invalid "\$" character in "\$ge". Query 4 identified an unclosed string or unrecognized token. Query 5 caught the invalid identifier "123.name" where identifiers cannot begin with numbers.

![Invalid query syntax](image-1.png)

Query 9 was successfully tokenized, displaying each part of a CREATE PROCEDURE statement properly identified as tokens (IDENTIFIER, PARAMETER, parentheses, etc.). Query 10 failed with an error message highlighting an unrecognized token "%" at position 38.

![Stored procedure syntax](image-2.png)
## Conclusions

The lexer implements the core principles of lexical analysis with a separation of concerns. It focuses solely on tokenization, which provides a solid foundation for subsequent parsing stages. The error handling system identifies and reports lexical errors with position information, which allows to make debugging easier. The indication of errors lets the user to deal faster with problematic inputs. The use of regular expressions The token identification process makes use of the regular expressions. The practical SQL query focus demonstrates real-world applicability, which handles SQL-specific elements like keywords (SELECT, FROM, WHERE), operators, identifiers, and string literals within actual query contexts. The next step would be to implement a parser which consumes these tokens to validate the syntactic structure according to the defined grammar rules.

## References

1. Formal Language & Automata Theory – Course Materials.