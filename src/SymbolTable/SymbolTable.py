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


    def is_function_existed(self, function_name):
        return function_name in self.function_symbol.keys()

    def add_function_name(self, identifier, return_type, parameter_num, parameter_type_list):
        if self.is_function_existed(identifier):
            pass # TODO 函数已存在错误
        else:
            self.function_symbol[identifier] = FunctionSymbol(identifier, return_type, parameter_num, parameter_type_list)

    def set_function_size(self, function_name, size):
        self.function_symbol[function_name].size = size

    def is_variable_existed(self, variable_name):
        return self.current_scope.is_variable_existed(variable_name)

    def add_variable_name(self, variable_name, variable_type):
        if self.is_variable_existed(variable_name):
            pass # TODO 变量已存在错误
        else:
            self.current_scope.add_variable_name(variable_name, variable_type, self.type_code[variable_type])

    def __str__(self):
        output = str(self.function_symbol)
        output += '\n'
        scope = self.current_scope
        while scope != None:
            for key, value in scope.variables.items():
                output += key
                output += "name: {} type: {} address: {}\n".format(key, value.type_name, value.address)
            output += '=============================\n'
            scope = scope.father_scope
        return output

