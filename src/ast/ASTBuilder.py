from resources.grammerParser import grammerParser
from resources.grammerLexer import grammerLexer

class ASTBuilder:
    current_function = None
    function_size = 0

    def __init__(self, tree: grammerParser.RContext, symbol_table):
        self.tree = tree
        self.symbol_table = symbol_table

    def build(self):
        self.build_translation_unit(self.tree.getChild(0))

    def build_translation_unit(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 2:
            self.build_translation_unit(tree.getChild(0))
            self.build_function_definition(tree.getChild(1))
        elif tree.getChildCount() == 1:
            self.build_function_definition(tree.getChild(0))

    def build_function_definition(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 3:
            return_type = self.build_declaration_specifiers(tree.getChild(0))
            self.build_function_declarator(tree.getChild(1))

    def build_declaration_specifiers(self, tree: grammerParser.RContext):
        return tree.getText()

    def build_function_declarator(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 3:
            function_name = self.build_function_name(tree.getChild(0))
            return function_name, []
        if(tree.getChildCount() == 4):
            function_name = self.build_function_name(tree.getChild(0))
            self.current_function = function_name
            parameter_type_list = self.build_parameter_list(tree.getChild(2))
            return function_name, parameter_type_list


    def build_function_name(self, tree: grammerParser.RContext):
        if tree.getPayload().type == grammerLexer.IDENTIFIER:
            return tree.getText()
        else:
            raise
        # TODO 出错处理

    def build_parameter_list(self, tree: grammerParser.RContext):
        parameter_type_list = []
        if tree.getChildCount() == 3:
            parameter_type_list = self.build_parameter_list(tree.getChild(0))
            parameter_type_list += self.build_parameter_declaration(tree.getChild(2))
        else:
            parameter_type_list += self.build_parameter_declaration(tree.getChild(0))
        return parameter_type_list

    def build_parameter_declaration(self, tree: grammerParser.RContext):
        pass
