# Laboratory Work No. 3

### Course: Formal Languages & Finite Automata  
### Author: Nicolae Marga
### Group: FAF-231

----

## Theory
Lexical analysis is the first phase of a compiler or interpreter that processes input text. It transforms a sequence of characters into a sequence of tokens that can be more easily processed by subsequent phases. The lexer operates by:

1. **Scanning** - Reading input characters one at a time
2. **Recognition** - Identifying lexemes (character sequences that form a logical unit)
3. **Classification** - Categorizing lexemes into token types
4. **Token generation** - Creating tokens with type and value information

In the context of programming languages, tokens typically include keywords, identifiers, literals, operators, and punctuation. Lexical analysis focuses solely on the structure of individual words or symbols in the input, without regard for their meaning or relationships.

## Objectives:

1. Design and implement a lexer:
   - Understand what lexical analysis is.
   - Get familiar with the inner workings of a lexer/scanner/tokenizer.
   - Implement a sample lexer and show how it works.

## Implementation description
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
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'NUMBER': r'\d+(\.\d+)?',
    'STRING': r'\'[^\']*\'',
    'COMMA': r',',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'WHITESPACE': r'\s+',
}
```

These patterns are combined into a master regex that matches all possible tokens:

```python
MASTER_REGEX = '|'.join(f'(?P<{key}>{value})' for key, value in TOKENS.items())
```

The named capture groups allow the lexer to identify which token type was matched.

### Core Lexer Implementation

The `QueryLexer` class encapsulates the lexical analysis process:

```python
class QueryLexer:
    def __init__(self, query):
        self.query = query
        self.position = 0

    def tokenize(self):
        tokens = []
        last_end_pos = 0
        
        # Check for empty query
        if not self.query:
            raise LexerError("Empty query", 0)
            
        for match in re.finditer(MASTER_REGEX, self.query):
            start_pos = match.start()
            
            # Check if there's any unrecognized content before this match
            if start_pos > last_end_pos:
                unrecognized = self.query[last_end_pos:start_pos]
                raise LexerError(f"Unrecognized token: '{unrecognized}'", last_end_pos)
                
            kind = match.lastgroup
            value = match.group()
            
            if kind == 'WHITESPACE':
                pass  # Ignore whitespace
            elif kind == 'STRING':
                # Check for unclosed quotes - this is still a tokenization issue
                if not (value.startswith("'") and value.endswith("'")):
                    raise LexerError("Malformed string literal", start_pos)
                value = value[1:-1]  # Remove quotes from string values
                tokens.append((kind, value))
            else:
                tokens.append((kind, value))
                
            last_end_pos = match.end()
        
        # Check if there's any unrecognized content at the end
        if last_end_pos < len(self.query):
            unrecognized = self.query[last_end_pos:]
            raise LexerError(f"Unrecognized token: '{unrecognized}'", last_end_pos)
            
        return tokens
```

The tokenization process:
1. Iterates through all regex matches in the input string
2. Checks for unrecognized characters between matches
3. Identifies token types based on which named group was matched
4. Handles special cases like whitespace (skipped) and strings (quotes removed)
5. Builds a list of tokens as (type, value) pairs

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

A helper function provides user-friendly error reporting:

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
    "SELECT name, age FROM users WHERE age > 18 AND city = 'New York'",  # Valid
    "SELECT name, @ge FROM users",  # Invalid character
    "SELECT name, age FROM users WHERE age > 18 AND city = 'New York",  # Unclosed string
    "SELECT 123name FROM users",  # Invalid identifier starting with number
    "$%^&",  # Invalid characters
    "",  # Empty query
]
```

## Conclusions

The lexer implements the core principles of lexical analysis with a separation of concerns. It focuses solely on tokenization, which provides a solid foundation for subsequent parsing stages. The error handling system identifies and reports lexical errors with position information, which allows to make debugging easier. The indication of errors lets the user to deal faster with problematic inputs. The use of regular expressions The token identification process makes use of the regular expressions. The practical SQL query focus demonstrates real-world applicability, which handles SQL-specific elements like keywords (SELECT, FROM, WHERE), operators, identifiers, and string literals within actual query contexts. The next step would be to implement a parser which consumes these tokens to validate the syntactic structure according to the defined grammar rules.