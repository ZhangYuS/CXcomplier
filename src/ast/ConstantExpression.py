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
        if self.type != 'bool':
            return ['ldc {} {}'.format(self.type_code[self.type], self.value)]
        else:
            if self.value:
                return ['ldc {} t'.format(self.type_code[self.type])]
            else:
                return ['ldc {} f'.format(self.type_code[self.type])]


    def get_code(self):
        return self.type_code[self.type]

    def get_type(self):
        return self.type

    def not_value(self):
        self.value = not self.value

    def negetive_value(self):
        self.value = -self.value

    def change_type(self):
        if self.type == 'int':
            self.type = 'real'
            self.value = float(self.value)
        elif self.type == 'real':
            self.type = 'int'
            self.value = int(self.value)