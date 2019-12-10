class ArithmeticExpression:

    type_code = {'int': 'i', 'bool': 'b', 'real': 'r'}


    def __init__(self, left_expressioin, right_expression, op):
        self.left_expression = left_expressioin
        self.right_expression = right_expression
        self.op = op
        self.type = self.left_expression.get_type()

    def get_type(self):
        return self.type

    def get_code(self):
        return self.type_code[self.type]

    def compiler(self):
        code = []
        left_expression = self.left_expression.compiler()
        right_expression = self.right_expression.compiler()
        if op == '%':
            code += left_expression
            code += left_expression
            code += right_expression
            code += ['div i']
            code += right_expression
            code += ['mul i']
            code += ['sub i']
            return code
        else:
            code += left_expression
            code += right_expression
            if self.op == '+':
                code.append(f'add {self.get_code()}')
            elif self.op == '-':
                code.append('sub {}'.format(self.get_code()))
            elif self.op == '*':
                code.append('mul {}'.format(self.get_code()))
            elif self.op == '/':
                code.append('div {}'.format(self.get_code()))
            return code


