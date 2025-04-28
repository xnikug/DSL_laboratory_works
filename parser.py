from tokens import Token, TokenType
from ast import ASTNode, SelectStatement, CreateProcedureStatement
from ast import Parameter, ColumnReference, WhereClause
from ast import BinaryOperation, LogicalOperation, Literal
from typing import List, Optional, Union
class ParserError(Exception):
    """Exception raised for errors during parsing."""
    def __init__(self, message, token=None):
        self.message = message
        self.token = token
        msg = f"{message}"
        if token:
            msg += f" at position {token.position}, token: {token.value}"
        super().__init__(msg)

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token_idx = 0
    
    def parse(self) -> ASTNode:
        """Parse the token stream and return an AST."""
        if not self.tokens:
            raise ParserError("No tokens to parse")
        
        # Look at the first token to determine the type of statement
        first_token = self.current_token()
        if first_token.type == TokenType.SELECT:
            return self.parse_select_statement()
        elif first_token.type == TokenType.CREATE:
            return self.parse_create_procedure()
        else:
            raise ParserError(f"Unexpected token at start of statement", first_token)
    
    def current_token(self) -> Optional[Token]:
        """Get the current token."""
        if self.current_token_idx < len(self.tokens):
            return self.tokens[self.current_token_idx]
        return None
    
    def advance(self) -> Optional[Token]:
        """Move to the next token and return it."""
        token = self.current_token()
        self.current_token_idx += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        """Expect the current token to be of a specific type, advance and return it."""
        token = self.current_token()
        if token is None:
            raise ParserError(f"Expected {token_type.name}, but reached end of input")
        if token.type != token_type:
            raise ParserError(f"Expected {token_type.name}, got {token.type.name}", token)
        
        self.advance()
        return token
    
    def parse_select_statement(self) -> SelectStatement:
        """Parse a SELECT statement."""
        # Expect SELECT keyword
        self.expect(TokenType.SELECT)
        
        # Parse column list
        columns = self.parse_column_list()
        
        # Expect FROM keyword
        self.expect(TokenType.FROM)
        
        # Parse table name
        table_token = self.expect(TokenType.IDENTIFIER)
        table_name = table_token.value
        
        # Parse optional WHERE clause
        where_clause = None
        if self.current_token() and self.current_token().type == TokenType.WHERE:
            self.advance()  # Consume WHERE token
            where_clause = self.parse_where_clause()
        
        return SelectStatement(columns, table_name, where_clause)
    
    def parse_column_list(self) -> List[ColumnReference]:
        """Parse a comma-separated list of column names."""
        columns = []
        
        # First column
        column_token = self.expect(TokenType.IDENTIFIER)
        columns.append(ColumnReference(column_token.value))
        
        # Additional columns
        while self.current_token() and self.current_token().type == TokenType.COMMA:
            self.advance()  # Consume comma
            column_token = self.expect(TokenType.IDENTIFIER)
            columns.append(ColumnReference(column_token.value))
        
        return columns
    
    def parse_where_clause(self) -> WhereClause:
        """Parse a WHERE clause."""
        condition = self.parse_condition()
        return WhereClause(condition)
    
    def parse_condition(self) -> Union[BinaryOperation, LogicalOperation]:
        """Parse a condition in a WHERE clause."""
        left = self.parse_expression()
        
        if not self.current_token():
            return left
        
        if self.current_token().type in [TokenType.AND, TokenType.OR]:
            operator = self.advance().value
            right = self.parse_condition()
            return LogicalOperation(left, operator, right)
        
        return left
    
    def parse_expression(self) -> BinaryOperation:
        """Parse a comparison expression."""
        left_token = self.expect(TokenType.IDENTIFIER)
        left = ColumnReference(left_token.value)
        
        operator_token = self.advance()
        if operator_token.type not in [TokenType.EQUALS, TokenType.GREATER, TokenType.LESS]:
            raise ParserError("Expected comparison operator", operator_token)
        
        operator = operator_token.value
        
        right_token = self.advance()
        if right_token.type == TokenType.NUMBER:
            right = Literal(float(right_token.value) if '.' in right_token.value else int(right_token.value), right_token.type)
        elif right_token.type == TokenType.STRING:
            right = Literal(right_token.value, right_token.type)
        elif right_token.type == TokenType.IDENTIFIER:
            right = ColumnReference(right_token.value)
        else:
            raise ParserError("Expected value or column reference", right_token)
        
        return BinaryOperation(left, operator, right)
    
    def parse_create_procedure(self) -> CreateProcedureStatement:
        """Parse a CREATE PROCEDURE statement."""
        # Expect CREATE and PROCEDURE keywords
        self.expect(TokenType.CREATE)
        self.expect(TokenType.PROCEDURE)
        
        # Parse procedure name
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        # Parse parameter list
        self.expect(TokenType.LPAREN)
        parameters = self.parse_parameter_list()
        self.expect(TokenType.RPAREN)
        
        # In a real implementation, you would parse the AS and BEGIN...END blocks
        # Here we'll just collect everything else as the "body" for simplicity
        body = "/* procedure body */"
        
        return CreateProcedureStatement (name, parameters, body)
    
    def parse_parameter_list(self) -> List[Parameter]:
        """Parse a comma-separated list of parameters."""
        parameters = []
        
        # First parameter (if exists)
        if self.current_token() and self.current_token().type == TokenType.PARAMETER:
            param_token = self.advance()
            parameters.append(Parameter(param_token.value))
            
            # Additional parameters
            while self.current_token() and self.current_token().type == TokenType.COMMA:
                self.advance()  # Consume comma
                param_token = self.expect(TokenType.PARAMETER)
                parameters.append(Parameter(param_token.value))
        
        return parameters