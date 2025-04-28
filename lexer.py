import re
from tokens import Token, TokenType, MASTER_REGEX
from typing import List
class LexerError(Exception):
    """Exception raised for errors during lexical analysis."""
    def __init__(self, message, position):
        self.message = message
        self.position = position
        super().__init__(f"{message} at position {position}")
class Lexer:
    def __init__(self, query):
        self.query = query
        self.position = 0
        self.tokens = []

    def tokenize(self) -> List[Token]:
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
                
            kind_name = match.lastgroup
            if kind_name == 'WHITESPACE':
                pass  # Ignore whitespace
            else:
                token_type = TokenType[kind_name]
                value = match.group()
                
                # Remove quotes from string values
                if token_type == TokenType.STRING:
                    if not (value.startswith("'") and value.endswith("'")):
                        raise LexerError("Malformed string literal", start_pos)
                    value = value[1:-1]  # Remove quotes from string values
                
                self.tokens.append(Token(token_type, value, start_pos))
                
            last_end_pos = match.end()
        
        # Check if there's any unrecognized content at the end
        if last_end_pos < len(self.query):
            unrecognized = self.query[last_end_pos:]
            raise LexerError(f"Unrecognized token: '{unrecognized}'", last_end_pos)
            
        return self.tokens