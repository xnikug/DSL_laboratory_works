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
    'NUMBER': r'\d+(\.\d+)?',
    'STRING': r'\'[^\']*\'',
    'COMMA': r',',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'WHITESPACE': r'\s+',
}

# Regular expression to match all token types in order of precedence
MASTER_REGEX = '|'.join(f'(?P<{key}>{value})' for key, value in TOKENS.items())

class Lexer:
    def __init__(self, query):
        self.query = query
        self.position = 0

    def tokenize(self):
        tokens = []
        for match in re.finditer(MASTER_REGEX, self.query):
            kind = match.lastgroup
            value = match.group()
            if kind == 'WHITESPACE':
                continue  # Ignore whitespace
            if kind == 'STRING':
                value = value[1:-1]  # Remove quotes from string values
            tokens.append((kind, value))
        return tokens

if __name__ == '__main__':
    query = "SELECT name, age FROM users WHERE age > 18 AND city = 'New York'"

    lexer = Lexer(query)
    tokens = lexer.tokenize()

    for token in tokens:
        print(token)
