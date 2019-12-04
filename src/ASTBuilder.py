from resources.grammerParser import grammerParser

class ASTBuilder:
    def __init__(self, tree: grammerParser.RContext, symbol_table):
        self.tree = tree
        self.symbol_table = symbol_table

    def build(self):
        self.build_translation_unit(self.tree.getChild(0))

    def build_function_declarator(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 3:
            function_name = tree.getChild(0)

    def build_declaration_specifiers(self, tree: grammerParser.RContext):
        return tree.getText()

    def build_function_definition(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 3:
            return_type = self.build_declaration_specifiers(tree.getChild(0))
            self.build_function_declarator(tree.getChild((1)))


    def build_translation_unit(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 2:
            self.build_translation_unit(tree.getChild(0))
            self.build_function_definition(tree.getChild(1))
        elif tree.getChildCount() == 1:
            self.build_function_definition(tree.getChild(0))