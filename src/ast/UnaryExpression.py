class UnaryExpression:

    type_code = {'int': 'i', 'bool': 'b', 'real': 'r'}

    def __init__(self, expression, op):
        self.op = op
        self.expression = expression
        self.type = expression.get_type()

    def compiler(self):
        code = self.expression.compiler()
        if self.op == '!':
            code.append('not')
        else:
            code.append('neg {}'.format(self.type_code[self.type]))
        return code

    def get_code(self):
        return self.type_code[self.get_type()]

    def get_type(self):
        return self.type
