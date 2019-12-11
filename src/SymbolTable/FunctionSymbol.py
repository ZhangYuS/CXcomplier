class FunctionSymbol:

    def __init__(self, identifier, return_type, parameter_number, parameter_type_list, size=0):
        self.identifier = identifier
        self.return_type = return_type
        self.parameter_number = parameter_number
        self.parameter_type_list = parameter_type_list
        self.size = size

    def get_function_size(self):
        return self.size

    def get_function_name(self):
        return self.identifier

    def get_function_type(self):
        return self.return_type

    def is_argument_right(self, expression_list):
        if len(expression_list) != self.parameter_number:
            return False
        for i in range(self.parameter_number):
            if expression_list[i].get_type() != self.parameter_type_list[i]:
                return False
        return True
