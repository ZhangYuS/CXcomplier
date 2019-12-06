from .Scope import Scope
from .Symbol import Symbol
from .FunctionSymbol import FunctionSymbol


class SymbolTable:

    def __init__(self):
        self.global_scope = Scope(None)
        self.current_scope = self.global_scope
        self.function_symbol = dict()
        self.type_code = {'int': 'i', 'bool': 'b', 'real': 'r'}

    def open_scope(self):
        self.current_scope = self.current_scope.open_scope()

    def close_scope(self):
        self.current_scope = self.current_scope.close_scope()

    def open_function_scope(self):
        self.current_scope = self.current_scope.open_function_scope()

    def close_function_scope(self):
        self.current_scope, size = self.current_scope.close_function_scope()
        return size
