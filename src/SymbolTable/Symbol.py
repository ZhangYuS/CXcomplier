class Symbol:

    def __init__(self, type_name, code, identifier, address):
        self.type_name = type_name
        self.code = code
        self.identifier = identifier
        self.address = address

    def get_identifier(self):
        return self.identifier

    def get_type(self):
        return self.type_name

    def get_address(self):
        return self.address
