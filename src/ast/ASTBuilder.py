from resources.grammerParser import grammerParser
from resources.grammerLexer import grammerLexer
from src.SymbolTable.SymbolTable import SymbolTable
from antlr4 import *

from .VariableExpression import VariableExpression
from .ConstantExpression import ConstantExpression
from .SelfIncrementPostfixExpression import SelfIncrementPostfixExpression
from .Function import Function


class ASTBuilder:

    def __init__(self, tree: grammerParser.RContext, symbol_table: SymbolTable):
        self.tree = tree
        self.symbol_table = symbol_table
        self.current_function = None

    def build(self):
        return self.build_translation_unit(self.tree.getChild(0))

    def build_translation_unit(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 2:
            function_list = self.build_translation_unit(tree.getChild(0))
            function_list += self.build_function_definition(tree.getChild(1))
            return function_list
        elif tree.getChildCount() == 1:
            return self.build_function_definition(tree.getChild(0))

    def build_function_definition(self, tree: grammerParser.RContext):
        self.symbol_table.open_function_scope()
        return_type = self.build_declaration_specifiers(tree.getChild(0))
        function_name, parameter_type_list = self.build_function_declarator(tree.getChild(1))
        self.current_function = function_name
        self.symbol_table.add_function_name(function_name, return_type, len(parameter_type_list), parameter_type_list)
        statement_list = self.build_compound_statement(tree.getChild(2))
        size = self.symbol_table.close_function_scope()
        self.symbol_table.set_function_size(self.current_function, size)
        function_symbol = self.symbol_table.get_function_symbol(self.current_function)
        return [Function(function_symbol, statement_list)]

    def build_declaration_specifiers(self, tree: grammerParser.RContext):
        return tree.getText()

    def build_function_declarator(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 3:
            function_name = self.build_function_name(tree.getChild(0))
            return function_name, []
        if tree.getChildCount() == 4:
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
        identifier_type = self.build_declaration_specifiers(tree.getChild(0))
        identifier_name = self.build_parameter_declarator(tree.getChild(1))
        self.symbol_table.add_variable_name(identifier_name, identifier_type)
        return [identifier_type]

    def build_parameter_declarator(self, tree: grammerParser.RContext):
        if tree.getChildCount() != 1:
            pass  # TODO 函数参数出错
        else:
            return tree.getText()

    def build_compound_statement(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 3:
            return self.build_statement_list(tree.getChild(1))
        else:
            pass # TODO 语句为空所做的事情

    def build_statement_list(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 2:
            statement_list = self.build_statement_list(tree.getChild(0))
            statement_list += self.build_statement(tree.getChild(1))
            return statement_list
        else:
            return [self.build_statement(tree.getChild(0))]

    def build_statement(self, tree: grammerParser.RContext):
        sub_tree: grammerParser.RContext = tree.getChild(0)
        if sub_tree.getRuleIndex() == grammerParser.RULE_expression_statement:
            return self.build_expression_statement(sub_tree)
        elif sub_tree.getRuleIndex() == grammerParser.RULE_declaration_statement:
            self.build_declaration_statement(sub_tree)
        elif sub_tree.getRuleIndex() == grammerParser.RULE_compound_statement:
            self.symbol_table.open_scope()
            self.build_compound_statement(sub_tree)
        else:
            self.build_output_statement(sub_tree)

    def build_expression_statement(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 2:
            return self.build_assignment_expression(tree.getChild(0))

    def build_assignment_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_logical_or_expression(tree.getChild(0))
        else:
            self.build_left_value_expression(tree.getChild(0))
            self.build_assignment_operator(tree.getChild(1))
            self.build_assignment_expression(tree.getChild(2))

    def build_assignment_operator(self, tree: grammerParser.RContext):
        return tree.getText()

    def build_logical_or_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_logical_and_expression(tree.getChild(0))
        else:
            self.build_logical_or_expression(tree.getChild(0))
            self.build_logical_and_expression(tree.getChild(2))

    def build_logical_and_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_equality_expression(tree.getChild(0))
        else:
            self.build_logical_and_expression(tree.getChild(0))
            self.build_equality_expression(tree.getChild(1))

    def build_equality_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_relational_expression(tree.getChild(0))
        else:
            self.build_equality_expression(tree.getChild(0))
            self.build_relational_expression(tree.getChild(2))

    def build_relational_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_additive_expression(tree.getChild(0))
        else:
            self.build_relational_expression(tree.getChild(0))
            self.build_additive_expression(tree.getChild(2))

    def build_additive_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_multiplicative_expression(tree.getChild(0))
        else:
            self.build_additive_expression(tree.getChild(0))
            self.build_multiplicative_expression(tree.getChild(2))

    def build_multiplicative_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_cast_expression(tree.getChild(0))
        else:
            self.build_multiplicative_expression(tree.getChild(0))
            self.build_cast_expression(tree.getChild(2))

    def build_cast_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_unary_expression(tree.getChild(0))
        else:
            self.build_declaration_specifiers(tree.getChild(1))
            self.build_cast_expression(tree.getChild(4))

    def build_unary_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_postfix_expression(tree.getChild(0))
        elif tree.getChild(0).getIndexRule == grammerParser.RULE_unary_operator:
            self.build_unary_operator(tree.getChild(0))
            self.build_cast_expression(tree.getChild(1))

    def build_unary_operator(self, tree: grammerParser.RContext):
        return tree.getText()

    def build_postfix_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_primary_expression(tree.getChild(0))
        elif tree.getChildCount() == 2:
            expression = self.build_postfix_expression(tree.getChild(0))
            if tree.getChild(1).getPayload().type == grammerLexer.INC_OP:
                if isinstance(expression, VariableExpression):
                    return SelfIncrementPostfixExpression(expression, tree.getChild(1).getText())
        elif tree.getChildCount() == 3:
            self.build_postfix_expression(tree.getChild(0))
        elif tree.getChild(1).getPayload().type == grammerLexer.LEFTSQUAREBRACKET:
            self.build_postfix_expression(tree.getChild(0))
            self.build_assignment_expression(tree.getChild(2))
        else:
            self.build_postfix_expression(tree.getChild(0))
            self.build_argument_expression_list(tree.getChild(2))

    def build_primary_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 3:
            return self.build_assignment_expression(tree.getChild(1))
        elif tree.getChild(0).getPayload().type == grammerLexer.INT_CONSTANT:
            return ConstantExpression(tree.getText(), 'int')
        elif tree.getChild(0).getPayload().type == grammerLexer.BOOL_CONSTANT:
            return ConstantExpression(tree.getText(), 'bool')
        elif tree.getChild(0).getPayload.type == grammerLexer.REAL_CONSTANT:
            return ConstantExpression(tree.getText(), 'real')
        else:
            if self.symbol_table.is_variable_existed(tree.getText()):
                type_name, address = self.symbol_table.get_variable(tree.getText())
                return VariableExpression(tree.getText(), type_name, address)

    def build_argument_expression_list(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            self.build_assignment_expression(tree.getChild(0))
        else:
            self.build_argument_expression_list(tree.getChild(0))
            self.build_assignment_expression(tree.getChild(2))

    def build_left_value_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return tree.getText()
        else:
            self.build_left_value_expression(tree.getChild(0))
            self.build_assignment_expression(tree.getChild(2))


    def build_declaration_statement(self, tree: grammerParser.RContext):
        pass

    def build_output_statement(self, tree: grammerParser.RContext):
        pass