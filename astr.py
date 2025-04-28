# AST Node Classes
from tokens import TokenType
class ASTNode:
    def __repr__(self):
        return self.__str__()

class SelectStatement(ASTNode):
    def __init__(self, columns, table_name, where_clause=None):
        self.columns = columns
        self.table_name = table_name
        self.where_clause = where_clause
    
    def __str__(self):
        result = f"SELECT {', '.join(str(col) for col in self.columns)} FROM {self.table_name}"
        if self.where_clause:
            result += f" WHERE {self.where_clause}"
        return result

class CreateProcedureStatement(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body
    
    def __str__(self):
        params_str = ', '.join(str(param) for param in self.parameters)
        return f"CREATE PROCEDURE {self.name}({params_str}) AS {self.body}"

class Parameter(ASTNode):
    def __init__(self, name, data_type=None):
        self.name = name
        self.data_type = data_type
    
    def __str__(self):
        if self.data_type:
            return f"{self.name} {self.data_type}"
        return self.name

class ColumnReference(ASTNode):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name

class WhereClause(ASTNode):
    def __init__(self, condition):
        self.condition = condition
    
    def __str__(self):
        return str(self.condition)

class BinaryOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"

class LogicalOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"

class Literal(ASTNode):
    def __init__(self, value, literal_type):
        self.value = value
        self.type = literal_type
    
    def __str__(self):
        if self.type == TokenType.STRING:
            return f"'{self.value}'"
        return str(self.value)