from src.SymbolTable.Symbol import Symbol


class VariableExpression:
    type_code = {'int': 'i', 'bool': 'b', 'real': 'r'}

    def __init__(self, variable: Symbol, expression_list=None):
        self.variable = variable
        self.array = variable.is_array()
        self.expression_list = expression_list

    def compiler(self, left_value=False):
        code = []
        if left_value:
            if self.array:
                code += ['lda 0 {}'.format(self.variable.get_address())]
                code += self.expression_list[-1].compiler()
                code += ['ixa 1']
                for i in range(len(self.expression_list) - 2, -1, -1):
                    code += self.expression_list[i].compiler()
                    code += ['ixa {}'.format(self.variable.get_length(i))]
            else:
                code += [f'str {self.type_code[self.variable.get_type()]} 0 {self.variable.get_address()}']
        else:
            if self.array:
                code += ['lda 0 {}'.format(self.variable.get_address())]
                code += self.expression_list[-1].compiler()
                code += ['ixa 1']
                for i in range(len(self.expression_list) - 2, -1, -1):
                    code += self.expression_list[i].compiler()
                    code += ['ixa {}'.format(self.variable.get_length(i))]
                code += ['ind {}'.format(self.type_code[self.variable.get_type()])]
            else:
                code += ['lod {} 0 {}'.format(self.type_code[self.variable.get_type()], self.variable.get_address())]
        return code

    def get_address(self):
        return self.variable.get_address()

    def get_code(self):
        return self.type_code[self.variable.get_type()]

    def get_type(self):
        return self.variable.get_type()

    def is_array(self):
        return self.array