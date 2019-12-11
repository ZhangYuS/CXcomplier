from src.SymbolTable.FunctionSymbol import FunctionSymbol

class Function:
    def __init__(self, function_symbol: FunctionSymbol, statement_list):
        self.function_symbol = function_symbol
        self.statement_list = statement_list

    def compiler(self):
        code = []
        code.append('{}:'.format(self.function_symbol.get_function_name()))
        code.append('ssp {}'.format(self.function_symbol.get_function_size()))
        for statement in self.statement_list:
            code += statement.compiler()
        return code