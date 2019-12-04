class FunctionSymbol:
    identifier = None
    return_type = None
    parameter_type_list = []
    parameter_number = 0
    address = 0
    size = 0

    def __init__(self, identifier, return_type, parameter_number, parameter_type_list, address, size):
        self.identifier = identifier
        self.return_type = return_type
        self.parameter_number = parameter_number
        self.parameter_type_list = parameter_type_list
        self.address = address
        self.size = size
