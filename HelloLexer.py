# Generated from .\Hello.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\5")
        buf.write("\30\b\1\4\2\t\2\4\3\t\3\4\4\t\4\3\2\7\2\13\n\2\f\2\16")
        buf.write("\2\16\13\2\3\3\3\3\3\4\6\4\23\n\4\r\4\16\4\24\3\4\3\4")
        buf.write("\2\2\5\3\3\5\4\7\5\3\2\4\3\2\62;\5\2\13\f\17\17\"\"\2")
        buf.write("\31\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\3\f\3\2\2\2\5")
        buf.write("\17\3\2\2\2\7\22\3\2\2\2\t\13\t\2\2\2\n\t\3\2\2\2\13\16")
        buf.write("\3\2\2\2\f\n\3\2\2\2\f\r\3\2\2\2\r\4\3\2\2\2\16\f\3\2")
        buf.write("\2\2\17\20\7-\2\2\20\6\3\2\2\2\21\23\t\3\2\2\22\21\3\2")
        buf.write("\2\2\23\24\3\2\2\2\24\22\3\2\2\2\24\25\3\2\2\2\25\26\3")
        buf.write("\2\2\2\26\27\b\4\2\2\27\b\3\2\2\2\5\2\f\24\3\b\2\2")
        return buf.getvalue()


class HelloLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    NUM = 1
    ADD = 2
    WS = 3

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'+'" ]

    symbolicNames = [ "<INVALID>",
            "NUM", "ADD", "WS" ]

    ruleNames = [ "NUM", "ADD", "WS" ]

    grammarFileName = "Hello.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


