class SelectionStatement:


    def __init__(self, condition, then_statement, start_label, else_statement = None, end_label = None):
        self.condition = condition
        self.then_statement = then_statement
        self.start_label = start_label
        self.else_statement = else_statement
        self.end_label = end_label

    def compiler(self):
        code = []
        code += self.condition.compiler()
        code += [f'fjp {self.start_label}']
        for statement in self.then_statement:
            code += statement.compiler()
        if self.else_statement is not None:
            code += [f'ujp {self.end_label}']
            code += [f'{self.start_label}:']
            for statement in self.else_statement:
                code += statement.compiler()
            code += [f'{self.end_label}:']
        else:
            code += [f'{self.start_label}:']
        return code