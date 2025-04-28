from enum import Enum, auto
# Define TokenType enum
class TokenType(Enum):
    SELECT = auto()
    FROM = auto()
    WHERE = auto()
    AND = auto()
    OR = auto()
    EQUALS = auto()
    GREATER = auto()
    LESS = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    COMMA = auto()
    LPAREN = auto()
    RPAREN = auto()
    CREATE = auto()
    PROCEDURE = auto()
    PARAMETER = auto()

# Define token types with their regular expressions
TOKEN_SPECS = {
    # Keywords
    TokenType.SELECT: r'\bSELECT\b',
    TokenType.FROM: r'\bFROM\b',
    TokenType.WHERE: r'\bWHERE\b',
    TokenType.AND: r'\bAND\b',
    TokenType.OR: r'\bOR\b',
    TokenType.CREATE: r'\bCREATE\b',
    TokenType.PROCEDURE: r'\bPROCEDURE\b',
    # Operators and symbols
    TokenType.EQUALS: r'=',
    TokenType.GREATER: r'>',
    TokenType.LESS: r'<',
    TokenType.IDENTIFIER: r'[a-zA-Z_][a-zA-Z0-9_]*|\*',
    TokenType.NUMBER: r'-?\d+(\.\d+)?',
    TokenType.STRING: r'\'[^\']*\'',
    TokenType.COMMA: r',',
    TokenType.LPAREN: r'\(',
    TokenType.RPAREN: r'\)',
    TokenType.PARAMETER: r'@[a-zA-Z_][a-zA-Z0-9_]*',
}
# Additional regex for whitespace
WHITESPACE_REGEX = r'\s+'

# Regular expression to match all token types in order of precedence
MASTER_REGEX = '|'.join(f'(?P<{token_type.name}>{regex})' for token_type, regex in TOKEN_SPECS.items())
MASTER_REGEX += f'|(?P<WHITESPACE>{WHITESPACE_REGEX})'
class Token:
    def __init__(self, token_type: TokenType, value: str, position: int):
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', pos={self.position})"


