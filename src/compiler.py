import sys
from antlr4 import *
from resources.grammerLexer import grammerLexer
from resources.grammerParser import grammerParser
from src.ast.ASTBuilder import ASTBuilder
from src.SymbolTable.SymbolTable import SymbolTable


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = grammerLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = grammerParser(stream)
    tree = parser.r()
    tree.getChildCount()
    symboltable = SymbolTable()
    astBuilder = ASTBuilder(tree, symboltable)
    ast = astBuilder.build()


if __name__ == '__main__':
    main(sys.argv)