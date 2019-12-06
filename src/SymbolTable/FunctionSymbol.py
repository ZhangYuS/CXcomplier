class FunctionSymbol:

    def __init__(self, identifier, return_type, parameter_number, parameter_type_list, size=0):
        self.identifier = identifier
        self.return_type = return_type
        self.parameter_number = parameter_number
        self.parameter_type_list = parameter_type_list
        self.size = size
