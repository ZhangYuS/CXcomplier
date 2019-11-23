import sys
from antlr4 import *
from antlr4.tree.Trees import Trees
from HelloLexer import HelloLexer
from HelloParser import HelloParser


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = HelloLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    tree = parser.r()
    buildExpression(tree)

def buildExpression(tree):
    if (tree.getChildCount() == 1):
        print("ldc i " + tree.getChild(0).getText())
    else:
        buildExpression(tree.getChild(0))
        buildExpression(tree.getChild(2))
        print("add i")



if __name__ == '__main__':
    main(sys.argv)