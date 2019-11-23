grammar Hello;
r  : expression ADD expression;
expression: NUM;
NUM : [0-9]*;
ADD : '+';
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines