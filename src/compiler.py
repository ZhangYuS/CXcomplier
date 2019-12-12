import sys
from antlr4 import *
from resources.grammerLexer import grammerLexer
from resources.grammerParser import grammerParser
from src.ast.ASTBuilder import ASTBuilder
from src.SymbolTable.SymbolTable import SymbolTable


def main(argv):
    pcode_file = open('pcode', 'w')
    input_stream = FileStream(argv[1])
    lexer = grammerLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = grammerParser(stream)
    tree = parser.r()
    tree.getChildCount()
    symboltable = SymbolTable()
    astBuilder = ASTBuilder(tree, symboltable)
    function_list = astBuilder.build()
    print('mst 0', file=pcode_file)
    print('cup 0 functionmain', file=pcode_file)
    print('hlt', file=pcode_file)
    for function in function_list:
        pcode = function.compiler()
        for line in pcode:
            print(line, file=pcode_file)


if __name__ == '__main__':
    main(sys.argv)