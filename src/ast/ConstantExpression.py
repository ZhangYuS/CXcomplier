class ConstantExpression:
    type_code = {'int': 'i', 'bool': 'b', 'real': 'r'}

    def __init__(self, value, type):
        if value == 'true':
            self.value = True
        elif value == 'false':
            self.value = False
        elif type == 'int':
            self.value = int(value)
        else:
            self.value = float(value)
        self.type = type

    def compiler(self):
        return ['ldc {} {}'.format(self.type_code[self.type], self.value)]

    def get_code(self):
        return self.type_code[self.type]

    def get_type(self):
        return self.type

    def not_value(self):
        self.value = not self.value

    def negetive_value(self):
        self.value = -self.value