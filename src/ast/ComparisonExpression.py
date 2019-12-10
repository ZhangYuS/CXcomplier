class ComparisonExpression:

    type_code = {'int': 'i', 'bool': 'b', 'real': 'r'}


    def __init__(self, left_expression, right_expression, op):
        self.left_expression = left_expression
        self.right_expression = right_expression
        self.op = op
        self.type = 'bool'

    def get_type(self):
        return self.type

    def get_code(self):
        return self.type_code[self.type]

    def compiler(self):
        code = []
        code += self.left_expression.compiler()
        code += self.right_expression.compiler()
        if self.op == '==':
            code += [f'equ {self.left_expression.get_code()}']
        elif self.op == '!=':
            code += [f'neq {self.left_expression.get_code()}']
        elif self.op == '>':
            code += [f'grt {self.left_expression.get_code()}']
        elif self.op == '<':
            code += [f'les {self.left_expression.get_code()}']
        elif self.op == '>=':
            code += [f'geq {self.left_expression.get_code()}']
        elif self.op == '<=':
            code += [f'leq {self.left_expression.get_code()}']
        elif self.op == '&&':
            code += [f'and']
        elif self.op == '||':
            code += ['or']
        return code

