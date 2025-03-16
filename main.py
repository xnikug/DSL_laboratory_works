import re

# Define token types
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
    'NUMBER': r'-?\d+(\.\d+)?',
    'STRING': r'\'[^\']*\'',
    'COMMA': r',',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'WHITESPACE': r'\s+',
}

# Regular expression to match all token types in order of precedence
MASTER_REGEX = '|'.join(f'(?P<{key}>{value})' for key, value in TOKENS.items())

class LexerError(Exception):
    """Exception raised for errors during lexical analysis."""
    def __init__(self, message, position):
        self.message = message
        self.position = position
        super().__init__(f"{message} at position {position}")

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
            print("Debug: " + str(match))
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
                print(value)
                tokens.append((kind, value))
                
            last_end_pos = match.end()
        
        # Check if there's any unrecognized content at the end
        if last_end_pos < len(self.query):
            unrecognized = self.query[last_end_pos:]
            raise LexerError(f"Unrecognized token: '{unrecognized}'", last_end_pos)
            
        return tokens

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
if __name__ == '__main__':

    # Testing the lexer with some sample queries
    queries = [
        "SELECT name, age FROM users WHERE age > 13213.8 AND city = 'New York'",  # Valid
        "SELECT name, @ge FROM users",  # Invalid character
        "SELECT name, age FROM users WHERE age > 18 AND city = 'New York",  # Unclosed string
        "SELECT 123name FROM users",  # Invalid identifier starting with number
        "$%^&",  # Invalid characters
        "",  # Empty query
        "SELECT name, age FROM users WHERE age > 18 AND city = 'New York' ",  # Unmathed quotes
    ]

    for i, query in enumerate(queries):
        print(f"\nQuery {i+1}: \"{query}\"")
        tokens = tokenize_query(query)
        if tokens:
            print("Tokens:")
            for token in tokens:
                print(token)