from .VariableExpression import VariableExpression
from .ArithmeticExpression import ArithmeticExpression

class AssignmentExpression:

    type_code = {'int': 'i', 'bool': 'b', 'real': 'r'}


    def __init__(self, variable_expression: VariableExpression, expression, op):
        self.variable_expression = variable_expression
        self.expression = expression
        self.op = op
        self.type = variable_expression.get_type()


    def get_type(self):
        return self.type

    def get_code(self):
        return self.type_code[self.type]

    def compiler(self):
        code = []
        if self.variable_expression.is_array():
            code += self.variable_expression.compiler(True)
            code += ['dpl a']
        if self.op == '=':
            code += self.expression.compiler()
        elif self.op == '*=':
            code += ArithmeticExpression(self.variable_expression, self.expression, '*').compiler()
        elif self.op == '/=':
            code += ArithmeticExpression(self.variable_expression, self.expression, '/').compiler()
        elif self.op == '%=':
            code += ArithmeticExpression(self.variable_expression, self.expression, '%').compiler()
        elif self.op == '+=':
            code += ArithmeticExpression(self.variable_expression, self.expression, '+').compiler()
        elif self.op == '-=':
            code += ArithmeticExpression(self.variable_expression, self.expression, '-').compiler()
        if self.variable_expression.is_array():
            code += [f'sto {self.variable_expression.get_code()}']
            code += [f'ind {self.variable_expression.get_code()}']
        else:
            code += [f'dpl {self.variable_expression.get_code()}']
            code += self.variable_expression.compiler(True)
        return code