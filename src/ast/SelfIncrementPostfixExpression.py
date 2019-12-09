from .VariableExpression import VariableExpression


class SelfIncrementPostfixExpression:
    def __init__(self, variable_expression: VariableExpression, op):
        self.variable_expression = variable_expression
        self.op = op

    def compiler(self):
        code = []
        code.append("dpl i")
        if self.op == '++':
            code.append('inc i 1')
        elif self.op == '--':
            code.append('dec i 1')
        code.append('str i 0 {}'.format(self.variable_expression.get_address()))
