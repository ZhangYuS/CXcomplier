class OutputStatement:
    def __init__(self, expression):
        self.expression = expression

    def compiler(self):
        code = []
        code += self.expression.compiler()
        code.append('out {}'.format(self.expression.get_code()))
        return code
