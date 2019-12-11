class ReturnStatement:

    def __init__(self, expression):
        self.expression = expression

    def compiler(self):
        code = []
        code += self.expression.compiler()
        code += [f'str {self.expression.get_code()} 0 0']
        code += ['retf']
        return code
