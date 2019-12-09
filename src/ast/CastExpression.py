class CastExpression:

    type_code = {'int': 'i', 'bool': 'b', 'real': 'r'}

    def __init__(self, expression, type):
        self.expression = expression
        self.type = type

    def get_type(self):
        return self.type

    def get_code(self):
        return self.type_code[self.type]

    def compiler(self):
        code = self.expression.compiler()
        code += 'conv {} {}'.format(self.expression.get_code(), self.get_code())
        return code