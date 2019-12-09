class VariableExpression:

    type_code = {'int': 'i', 'bool': 'b', 'real': 'r'}

    def __init__(self, identifier, type, address):
        self.identifier = identifier
        self.type = type
        self.address = address

    def compiler(self):
        return ['lod {} 0 {}'.format(self.type_code[self.type], self.address)]

    def get_address(self):
        return self.address

    def get_code(self):
        return self.type_code[self.type]

    def get_type(self):
        return self.type