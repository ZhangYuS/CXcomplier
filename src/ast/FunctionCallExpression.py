from src.SymbolTable.FunctionSymbol import FunctionSymbol

class FunctionCallExpression:

    type_code = {'int': 'i', 'bool': 'b', 'real': 'r'}

    def __init__(self, function_symbol: FunctionSymbol, argument_expression_list=[]):
        self.function_symbol = function_symbol
        self.argument_expression_list = argument_expression_list

    def compiler(self):
        code = []
        code += ['mst 0']
        for expression in self.argument_expression_list:
            code += expression.compiler()
        code += [f'cup {len(self.argument_expression_list)} function{self.function_symbol.get_function_name()}']
        return code

    def get_type(self):
        return self.function_symbol.get_function_type()

    def get_code(self):
        return self.type_code[self.function_symbol.get_function_type()]