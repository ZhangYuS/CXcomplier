from .VariableExpression import VariableExpression


class SelfIncrementPostfixExpression:
    def __init__(self, variable_expression: VariableExpression, op):
        self.variable_expression = variable_expression
        self.op = op

    def compiler(self):
        code = []
        code += self.variable_expression.compiler()
        if self.variable_expression.is_array():
            self.variable_expression.compiler(True)
        code.append("dpl i")
        if self.op == '++':
            code.append('inc i 1')
        elif self.op == '--':
            code.append('dec i 1')
        if self.variable_expression.is_array():
            code.append('str i')
        else:
            code += self.variable_expression.compiler(True)
        return code

    def get_code(self):
        return 'i'