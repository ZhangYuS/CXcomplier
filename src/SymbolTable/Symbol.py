class Symbol:

    def __init__(self, identifier, type_name, code, address, size_list=None):
        self.type_name = type_name
        self.code = code
        self.identifier = identifier
        self.address = address
        if size_list is not None:
            self.array = True
            self.size_list = size_list
        else:
            self.array = False

    def get_identifier(self):
        return self.identifier

    def get_type(self):
        return self.type_name

    def get_address(self):
        return self.address

    def is_array(self):
        return self.array

    def get_length(self, d):
        ret = 1
        for i in range(d, len(self.size_list)):
            ret *= self.size_list[i]
        return ret
