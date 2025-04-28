from tokens import Token, TokenType
from lexer import Lexer, LexerError
from typing import List, Optional, Tuple





def main():
    # Test queries from the original code plus some additional ones
    queries = [
        "SELECT name, age FROM users WHERE age > 21 AND city = 'New York' AND test = 'TEST'",  # Valid
        "SELECT * FROM users",  # Valid with wildcard
        "SELECT name FROM users WHERE age = 18",  # Valid simple condition
        "SELECT name, age FROM users WHERE age > 18 AND city = 'Washington",  # Unclosed string
        "CREATE PROCEDURE myProc(@param1, @param2) AS BEGIN SELECT * FROM users END",  # Simplified stored procedure
        "SELECT $%^ FROM users",  # Invalid syntax
        "SELECT FROM users WHERE age > 18",  # Missing columns
    ]
if __name__ == '__main__':
    main()