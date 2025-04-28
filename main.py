from tokens import Token, TokenType
from lexer import Lexer, LexerError
from astr import ASTNode
from parser import Parser, ParserError
from typing import List, Optional, Tuple



def analyze_query(query: str) -> Tuple[List[Token], Optional[ASTNode]]:
    """Process a query through lexical analysis and parsing."""
    try:
        # Lexical analysis
        lexer = Lexer(query)
        tokens = lexer.tokenize()
        
        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        
        return tokens, ast
    except LexerError as e:
        print(f"Lexer Error: {e}")
        if query:
            print(query)
            print(' ' * e.position + '^')
        return [], None
    except ParserError as e:
        print(f"Parser Error: {e}")
        return tokens, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return [], None

def print_ast_tree(node, indent="", is_last=True):
    """Print an AST as a tree structure."""
    # Determine the branch symbol
    branch = "└── " if is_last else "├── "
    
    # Print the current node with proper indentation
    print(f"{indent}{branch}{node.__class__.__name__}")
    
    # Determine the new indentation for children
    new_indent = indent + ("    " if is_last else "│   ")
    
    # Get all attributes of the node that are ASTNodes or lists/dicts containing ASTNodes
    children = []
    for attr_name, attr_value in node.__dict__.items():
        if isinstance(attr_value, ASTNode):
            children.append((attr_name, attr_value))
        elif isinstance(attr_value, list) and attr_value and isinstance(attr_value[0], ASTNode):
            # For lists of nodes (like columns in a SELECT statement)
            for i, item in enumerate(attr_value):
                children.append((f"{attr_name}[{i}]", item))
        elif not isinstance(attr_value, (ASTNode, list)) and attr_value is not None:
            # Print simple values directly
            value_branch = "└── " if not children else "├── "
            print(f"{new_indent}{value_branch}{attr_name}: {attr_value}")
    
    # Recursively print children
    for i, (attr_name, child) in enumerate(children):
        is_last_child = i == len(children) - 1
        label_indent = new_indent
        print(f"{label_indent}{'└── ' if is_last_child else '├── '}{attr_name}:")
        print_ast_tree(child, label_indent + ("    " if is_last_child else "│   "), True)

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

    for i, query in enumerate(queries):
        print(f"\nQuery {i+1}: \"{query}\"")
        tokens, ast = analyze_query(query)
        
        if tokens:
            print("Tokens:")
            for token in tokens:
                print(token)
        
        if ast:
            print("\nAbstract Syntax Tree:")
            print(f"String representation: {ast}")
            print("\nTree visualization:")
            print_ast_tree(ast)
        
        print("-" * 50)

if __name__ == '__main__':
    main()