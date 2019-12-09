class ConstantExpression:
    type_code = {'int': 'i', 'bool': 'b', 'real': 'r'}

    def __init__(self, value, type):
        if value == 'true':
            self.value = 't'
        elif value == 'false':
            self.value = 'f'
        else:
            self.value = value
        self.type = type

    def compiler(self):
        return ['ldc {} {}'.format(self.type_code[self.type], self.value)]