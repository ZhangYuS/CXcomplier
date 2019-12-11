class PcodeExpression:
    def __init__(self, pcode_list):
        self.pcode_list = pcode_list

    def compiler(self):
        return self.pcode_list