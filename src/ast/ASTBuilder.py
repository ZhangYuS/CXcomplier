from functools import reduce

from resources.grammerParser import grammerParser
from resources.grammerLexer import grammerLexer
from src.SymbolTable.SymbolTable import SymbolTable
from antlr4 import *

from .VariableExpression import VariableExpression
from .ConstantExpression import ConstantExpression
from .SelfIncrementPostfixExpression import SelfIncrementPostfixExpression
from .Function import Function
from .OutputStatement import OutputStatement
from .SelfIncrementUnaryExpression import SelfIncrementUnaryExpression
from .UnaryExpression import UnaryExpression
from .CastExpression import CastExpression
from .ArithmeticExpression import ArithmeticExpression
from .ComparisonExpression import ComparisonExpression
from .AssignmentExpression import AssignmentExpression
from .PcodeExpression import PcodeExpression
from .FunctionCallExpression import FunctionCallExpression
from .ReturnStatement import ReturnStatement
from .SelectionStatement import SelectionStatement
from .IterationStatement import IterationStatement


class ASTBuilder:

    def __init__(self, tree: grammerParser.RContext, symbol_table: SymbolTable):
        self.tree = tree
        self.symbol_table = symbol_table
        self.current_function = None
        self.label = 0

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
            pass  # TODO 语句为空所做的事情

    def build_statement_list(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 2:
            statement_list = self.build_statement_list(tree.getChild(0))
            statement_list += self.build_statement(tree.getChild(1))
            return statement_list
        else:
            return self.build_statement(tree.getChild(0))

    def build_statement(self, tree: grammerParser.RContext):
        sub_tree: grammerParser.RContext = tree.getChild(0)
        if sub_tree.getRuleIndex() == grammerParser.RULE_expression_statement:
            return [self.build_expression_statement(sub_tree)]
        elif sub_tree.getRuleIndex() == grammerParser.RULE_declaration_statement:
            return self.build_declaration_statement(sub_tree)
        elif sub_tree.getRuleIndex() == grammerParser.RULE_compound_statement:
            self.symbol_table.open_scope()
            ret = self.build_compound_statement(sub_tree)
            self.symbol_table.close_scope()
            return ret
        elif sub_tree.getRuleIndex() == grammerParser.RULE_return_statement:
            return [self.build_return_statement(sub_tree)]
        elif sub_tree.getRuleIndex() == grammerParser.RULE_output_statement:
            return [self.build_output_statement(sub_tree)]
        elif sub_tree.getRuleIndex() == grammerParser.RULE_selection_statement:
            return [self.build_seletion_statement(sub_tree)]
        elif sub_tree.getRuleIndex() == grammerParser.RULE_iteration_statement:
            return [self.build_iteration_statement(sub_tree)]

    def build_expression_statement(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 2:
            return self.build_assignment_expression(tree.getChild(0))

    def build_assignment_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_logical_or_expression(tree.getChild(0))
        else:
            identifier, expression_list = self.build_variable_expression(tree.getChild(0))
            op = self.build_assignment_operator(tree.getChild(1))
            expression = self.build_assignment_expression(tree.getChild(2))
            if self.symbol_table.is_variable_existed(identifier):
                symbol = self.symbol_table.get_variable(identifier)
                if symbol.get_type() == expression.get_type():
                    if len(expression_list) > 0:
                        variable_expression = VariableExpression(symbol, expression_list)
                    else:
                        variable_expression = VariableExpression(symbol)
                    return AssignmentExpression(variable_expression, expression, op)
                else:
                    pass  # TODO 变量类型不符
            else:
                pass  # TODO 变量未定义

    def build_assignment_operator(self, tree: grammerParser.RContext):
        return tree.getText()

    def build_logical_or_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_logical_and_expression(tree.getChild(0))
        else:
            left_expression = self.build_logical_or_expression(tree.getChild(0))
            right_expression = self.build_logical_and_expression(tree.getChild(2))
            op = tree.getChild(1).getText()
            if left_expression.get_type() == right_expression.get_type() and left_expression.get_type() == 'bool':
                return ComparisonExpression(left_expression, right_expression, op)

    def build_logical_and_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_equality_expression(tree.getChild(0))
        else:
            left_expression = self.build_logical_and_expression(tree.getChild(0))
            right_expression = self.build_equality_expression(tree.getChild(1))
            op = tree.getChild(1).getText()
            if left_expression.get_type() == right_expression.get_type() and left_expression.get_type() == 'bool':
                return ComparisonExpression(left_expression, right_expression, op)

    def build_equality_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_relational_expression(tree.getChild(0))
        else:
            left_expression = self.build_equality_expression(tree.getChild(0))
            right_expression = self.build_relational_expression(tree.getChild(2))
            op = tree.getChild(1).getText()
            if left_expression.get_type() == right_expression.get_type():
                return ComparisonExpression(left_expression, right_expression, op)

    def build_relational_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_additive_expression(tree.getChild(0))
        else:
            left_expression = self.build_relational_expression(tree.getChild(0))
            right_expression = self.build_additive_expression(tree.getChild(2))
            op = tree.getChild(1).getText()
            if left_expression.get_type() == right_expression.get_type() and left_expression.get_type() != 'bool':
                return ComparisonExpression(left_expression, right_expression, op)

    def build_additive_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_multiplicative_expression(tree.getChild(0))
        else:
            left_expression = self.build_additive_expression(tree.getChild(0))
            right_expression = self.build_multiplicative_expression(tree.getChild(2))
            op = tree.getChild(1).getText()
            if left_expression.get_type() == right_expression.get_type() and left_expression.get_type() != 'bool':
                if isinstance(left_expression, ConstantExpression) and isinstance(right_expression, ConstantExpression):
                    if op == '+':
                        return ConstantExpression(left_expression.get_value() + right_expression.get_value(),
                                                  left_expression.get_type())
                    if op == '-':
                        return ConstantExpression(left_expression.get_value() - right_expression.get_value(),
                                                  left_expression.get_type())
                else:
                    return ArithmeticExpression(left_expression, right_expression, op)
            else:
                pass  # TODO 类型出错

    def build_multiplicative_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_cast_expression(tree.getChild(0))
        else:
            left_expression = self.build_multiplicative_expression(tree.getChild(0))
            right_expression = self.build_cast_expression(tree.getChild(2))
            op = tree.getChild(1).getText()
            if left_expression.get_type() == right_expression.get_type() and left_expression.get_type() != 'bool':
                if isinstance(left_expression, ConstantExpression) and isinstance(right_expression, ConstantExpression):
                    if op == '*':
                        return ConstantExpression(left_expression.get_value() * right_expression.get_value(),
                                                  left_expression.get_type())
                    if left_expression.get_type() == 'int':
                        if op == '/':
                            return ConstantExpression(left_expression.get_value() // right_expression.get_value(),
                                                      left_expression.get_type())
                        elif op == '%':
                            return ConstantExpression(left_expression.get_value() % right_expression.get_value(),
                                                      left_expression.get_type())
                    else:
                        if op == '/':
                            return ConstantExpression(left_expression.get_value() / right_expression.get_value(),
                                                      left_expression.get_type())
                        else:
                            pass  # TODO 类型出错


                else:
                    pass
                if op != '%' and left_expression.get_type() == 'real':
                    pass  # TODO 类型不匹配

                else:
                    return ArithmeticExpression(left_expression, right_expression, op)


            else:
                pass  # TODO 类型不匹配

    def build_cast_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_unary_expression(tree.getChild(0))
        else:
            expression = self.build_cast_expression(tree.getChild(3))
            type = self.build_declaration_specifiers(tree.getChild(1))
            if expression.get_type() != type:
                if type == 'bool' or expression.get_type() == 'bool':
                    pass  # TODO bool 类型无法转化
                else:
                    if isinstance(expression, ConstantExpression):
                        expression.change_type()
                        return expression
                    else:
                        return CastExpression(expression, type)

    def build_unary_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return self.build_postfix_expression(tree.getChild(0))
        elif tree.getChild(0).getChildCount() > 0:
            op = self.build_unary_operator(tree.getChild(0))
            expression = self.build_cast_expression(tree.getChild(1))
            if op == 'not':
                if expression.get_type() == 'bool':
                    if isinstance(expression, ConstantExpression):
                        expression.not_value()
                        return expression
                    else:
                        return UnaryExpression(expression, op)
                else:
                    pass  # TODO not 后面只能是 bool 类型
            elif op == '-':
                if expression.get_type() != 'bool':
                    if isinstance(expression, ConstantExpression):
                        expression.negetive_value()
                        return expression
                    else:
                        return UnaryExpression(expression, op)
                else:
                    pass  # TODO 负号后面只能是整形或浮点型
        else:
            expression = self.build_unary_expression(tree.getChild(1))
            if isinstance(expression, VariableExpression) and expression.get_type() == 'int':
                return SelfIncrementUnaryExpression(expression, tree.getChild(0).getText())
            else:
                pass  # TODO 类型不符

    def build_unary_operator(self, tree: grammerParser.RContext):
        return tree.getText()

    def build_postfix_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            expression = self.build_primary_expression(tree.getChild(0))
            return expression
        elif tree.getChildCount() == 2:
            expression = self.build_postfix_expression(tree.getChild(0))
            if isinstance(expression, VariableExpression) and expression.get_type() == 'int':
                return SelfIncrementPostfixExpression(expression, tree.getChild(1).getText())
            else:
                pass  # TODO 错误
        elif tree.getChildCount() == 3:
            function_name = self.build_postfix_expression(tree.getChild(0))
            if self.symbol_table.is_function_existed(function_name):
                function_symbol = self.symbol_table.get_function_symbol(function_name)
                if function_symbol.is_argument_right([]):
                    return FunctionCallExpression(function_symbol, [])
                else:
                    pass  # TODO 函数参数不符
            else:
                pass  # TODO 未定义函数
        else:
            function_name = self.build_postfix_expression(tree.getChild(0))
            argument_expression_list = self.build_argument_expression_list(tree.getChild(2))
            if self.symbol_table.is_function_existed(function_name):
                function_symbol = self.symbol_table.get_function_symbol(function_name)
                if function_symbol.is_argument_right(argument_expression_list):
                    return FunctionCallExpression(function_symbol, argument_expression_list)
                else:
                    pass  # TODO 函数参数不符

            else:
                pass  # TODO 未定义函数

    def build_primary_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 3:
            return self.build_assignment_expression(tree.getChild(1))
        elif tree.getChild(0).getChildCount() != 0:
            identifier, expression_list = self.build_variable_expression(tree.getChild(0))
            if self.symbol_table.is_function_existed(identifier) and len(expression_list) == 0:
                return identifier
            if self.symbol_table.is_variable_existed(identifier):
                symbol = self.symbol_table.get_variable(identifier)
                if len(expression_list) > 0:
                    variable_expression = VariableExpression(symbol, expression_list)
                else:
                    variable_expression = VariableExpression(symbol)
                return variable_expression
            else:
                pass  # TODO 变量未定义
        elif tree.getChild(0).getPayload().type == grammerLexer.INT_CONSTANT:
            return ConstantExpression(tree.getText(), 'int')
        elif tree.getChild(0).getPayload().type == grammerLexer.BOOL_CONSTANT:
            return ConstantExpression(tree.getText(), 'bool')
        elif tree.getChild(0).getPayload().type == grammerLexer.REAL_CONSTANT:
            return ConstantExpression(tree.getText(), 'real')

    def build_argument_expression_list(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return [self.build_assignment_expression(tree.getChild(0))]
        else:
            argument_expression_list = self.build_argument_expression_list(tree.getChild(0))
            argument_expression_list += self.build_assignment_expression(tree.getChild(2))

    def build_variable_expression(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            return tree.getText(), []
        else:
            identifier, expression_list = self.build_variable_expression(tree.getChild(0))
            expression_list.append(self.build_assignment_expression(tree.getChild(2)))
            return identifier, expression_list

    def build_declaration_statement(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 3:
            type = self.build_declaration_specifiers(tree.getChild(0))
            return self.build_init_declarator_list(tree.getChild(1), type)

    def build_init_declarator_list(self, tree: grammerParser.RContext, type):
        if tree.getChildCount() == 3:
            expression_list = self.build_init_declarator_list(tree.getChild(0), type)
            expression_list += self.build_init_declarator(tree.getChild(2), type)
            return expression_list
        if tree.getChildCount() == 1:
            return [self.build_init_declarator(tree.getChild(0), type)]

    def build_init_declarator(self, tree: grammerParser.RContext, type):
        if tree.getChildCount() == 3:
            identifier, size_list = self.build_declarator(tree.getChild(0))
            if len(size_list) > 0:
                pass  # TODO 数组无法赋初值
            else:
                self.symbol_table.add_variable_name(identifier, type)
            variable_expression = VariableExpression(self.symbol_table.get_variable(identifier))
            expression = self.build_assignment_expression(tree.getChild(2))
            if variable_expression.get_type() != expression.get_type():
                pass  # TODO 类型出错
            return AssignmentExpression(variable_expression, expression, '=')
        else:
            identifier, size_list = self.build_declarator(tree.getChild(0))
            if len(size_list) > 0:
                self.symbol_table.add_variable_name(identifier, type, size_list)
                symbol = self.symbol_table.get_variable(identifier)
                code = []
                length = reduce(lambda x, y: x * y, size_list)
                for i in range(length):
                    code += [f'lda 0 {symbol.get_address()}']
                    code += [f'ldc i {i}']
                    code += [f'ixa 1']
                    if symbol.get_type() == 'int':
                        code += [f'ldc i 0']
                        code += [f'sto i']
                    elif symbol.get_type() == 'real':
                        code += [f'ldc r 0.0']
                        code += [f'sto r']
                    elif symbol.get_type() == 'bool':
                        code += [f'ldc b f']
                        code += [f'sto b']
                return PcodeExpression(code)
            else:
                self.symbol_table.add_variable_name(identifier, type)
                variable_expression = VariableExpression(self.symbol_table.get_variable(identifier))
                if type == 'int':
                    expression = ConstantExpression('0', 'int')
                elif type == 'real':
                    expression = ConstantExpression('0.0', 'real')
                else:
                    expression = ConstantExpression('false', 'bool')
                return AssignmentExpression(variable_expression, expression, '=')

    def build_declarator(self, tree: grammerParser.RContext):
        if tree.getChildCount() == 1:
            identifier = tree.getText()
            return identifier, []
        elif tree.getChildCount() == 4 and tree.getChild(0).getRuleIndex() == grammerParser.RULE_declarator:
            identifier, size_list = self.build_declarator(tree.getChild(0))
            expression = self.build_logical_or_expression(tree.getChild(2))
            if isinstance(expression, ConstantExpression) and expression.get_type() == 'int':
                size_list.append(expression.get_value())
            return identifier, size_list

    def build_output_statement(self, tree: grammerParser.RContext):
        expression = self.build_expression_statement(tree.getChild(1))
        return OutputStatement(expression)

    def build_return_statement(self, tree: grammerParser.RContext):
        expression = self.build_assignment_expression(tree.getChild(1))
        if expression.get_type() == self.symbol_table.get_function_symbol(self.current_function).get_function_type():
            return ReturnStatement(expression)
        else:
            pass  # TODO 返回类型不符

    def build_seletion_statement(self, tree: grammerParser.RContext):
        condition = self.build_assignment_expression(tree.getChild(2))
        if condition.get_type() != 'bool':
            pass # TODO 条件为 bool 值
        then_statement = self.build_statement(tree.getChild(4))
        if not isinstance(then_statement, list):
            then_statement = [then_statement]
        if tree.getChildCount() == 7:
            else_statement = self.build_statement(tree.getChild(6))
            if not isinstance(else_statement, list):
                else_statement = [else_statement]
            self.label += 2
            return SelectionStatement(condition, then_statement, 'label'+str(self.label - 2), else_statement, 'label'+str(self.label - 1))
        else:
            self.label += 1
            return SelectionStatement(condition, then_statement, 'label'+str(self.label - 1))

    def build_iteration_statement(self, tree: grammerParser.RContext):
        self.label += 2
        if tree.getChild(0).getText() == 'while':
            condition = self.build_assignment_expression(tree.getChild(2))
            if condition.get_type() != 'bool':
                pass # TODO 条件为 bool
            after_before = self.build_statement(tree.getChild(4))
            if not isinstance(after_before, list):
                after_before = [after_before]
            return IterationStatement(condition, f'label{self.label - 2}', f'label{self.label - 1}', [], after_before, [])
