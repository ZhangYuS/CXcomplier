class IterationStatement:
    def __init__(self, condition, begin_label, end_label, before_start, after_start, before_end):
        self.condition = condition
        self.begin_label = begin_label
        self.end_label = end_label
        self.before_start = before_start
        self.after_start = after_start
        self.before_end = before_end

    def compiler(self):
        code = []
        for statement in self.before_start:
            code += statement.compiler()
        code += [f'{self.begin_label}:']
        code += self.condition.compiler()
        code += [f'fjp {self.end_label}']
        for statement in self.after_start:
            code += statement.compiler()
        for statement in self.before_end:
            code += statement.compiler()
        code += [f'ujp {self.begin_label}']
        code += [f'{self.end_label}:']
        return code
