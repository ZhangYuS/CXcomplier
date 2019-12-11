grammar grammer;
r   :
    translation_unit
    ;

translation_unit
    : function_definition
    | translation_unit function_definition
    ;

function_definition
    : declaration_specifiers declarator compound_statement
    ;

declaration_specifiers
    : INT
    | BOOL
    | REAL
    ;

declarator
    : IDENTIFIER
    | IDENTIFIER LEFTPARENTHESIS parameter_list RIGHTPARENTHESIS
    | IDENTIFIER LEFTPARENTHESIS RIGHTPARENTHESIS
    | declarator LEFTSQUAREBRACKET logical_or_expression RIGHTSQUAREBRACKET
    ;

parameter_list
    : parameter_list COMMA parameter_declaration
    | parameter_declaration
    ;

parameter_declaration
    : declaration_specifiers declarator
    ;

compound_statement
    : LEFTBRACE statement_list RIGHTBRACE
    | LEFTBRACE RIGHTBRACE
    ;

declaration_statement
    : declaration_specifiers SEMICOLON
    | declaration_specifiers init_declarator_list SEMICOLON
    ;

init_declarator_list
    : init_declarator
    | init_declarator_list COMMA init_declarator
    ;

init_declarator
    : declarator
    | declarator ASSIGN assignment_expression
    ;

statement_list
    : statement
    | statement_list statement
    ;

statement
    : expression_statement
    | declaration_statement
    | compound_statement
    | output_statement
    | return_statement
    | selection_statement
    ;

expression_statement
    : assignment_expression SEMICOLON
    | SEMICOLON
    ;

assignment_expression
    : logical_or_expression
    | variable_expression assignment_operator assignment_expression
    ;

assignment_operator
    : ASSIGN
    | MUL_ASSIGN
    | DIV_ASSIGN
    | MOD_ASSIGN
    | ADD_ASSIGN
    | SUB_ASSIGN
    ;

logical_or_expression
    : logical_and_expression
    | logical_or_expression OR_OP logical_and_expression
    ;

logical_and_expression
    : equality_expression
    | logical_and_expression AND_OP equality_expression
    ;

equality_expression
    : relational_expression
    | equality_expression EQ_OP relational_expression
    | equality_expression NE_OP relational_expression
    ;

relational_expression
    : additive_expression
    | relational_expression LESSTHAN additive_expression
    | relational_expression GREATERTHAN additive_expression
    | relational_expression LE_OP additive_expression
    | relational_expression GE_OP additive_expression
    ;

additive_expression
    : multiplicative_expression
    | additive_expression PLUS multiplicative_expression
    | additive_expression MINUS multiplicative_expression
    ;

multiplicative_expression
    : cast_expression
    | multiplicative_expression MUL cast_expression
    | multiplicative_expression DIV cast_expression
    | multiplicative_expression MOD cast_expression
    ;

cast_expression
    : LEFTPARENTHESIS declaration_specifiers RIGHTPARENTHESIS cast_expression
    | unary_expression
    ;


unary_expression
    : postfix_expression
    | INC_OP unary_expression
    | DEC_OP unary_expression
    | unary_operator cast_expression
    ;

unary_operator
    : PLUS
    | MINUS
    | NOT
    ;

postfix_expression
    : primary_expression
    | postfix_expression LEFTPARENTHESIS RIGHTPARENTHESIS
    | postfix_expression LEFTPARENTHESIS argument_expression_list RIGHTPARENTHESIS
    | postfix_expression INC_OP
    | postfix_expression DEC_OP
    ;

argument_expression_list
    : assignment_expression
    | argument_expression_list COMMA assignment_expression
    ;

primary_expression
    : variable_expression
    | INT_CONSTANT
    | BOOL_CONSTANT
    | REAL_CONSTANT
    | LEFTPARENTHESIS assignment_expression RIGHTPARENTHESIS
    ;

variable_expression
    : IDENTIFIER
    | variable_expression LEFTSQUAREBRACKET assignment_expression RIGHTSQUAREBRACKET
    ;

output_statement
    : OUTPUT expression_statement
    ;

return_statement
    : RETURN assignment_expression SEMICOLON
    ;

selection_statement
    : IF LEFTPARENTHESIS assignment_expression RIGHTPARENTHESIS statement ELSE statement
    | IF LEFTPARENTHESIS assignment_expression RIGHTPARENTHESIS statement
    ;

COMMENT
: (BEGININLINECOMMENT .*? NEWLINE
| BEGINCOMMENT .*? ENDCOMMENT) -> skip
;

WHITESPACE: (' '|'\t')+ -> skip;
NEWLINE: '\r'? '\n' -> skip;


FOR: 'for';
IF: 'if';
INT: 'int';
RETURN: 'return';
WHILE: 'while';
BOOL: 'bool';
REAL: 'real';
BOOL_CONSTANT: 'true' | 'false';
OUTPUT: 'write';
ELSE: 'else';


INT_CONSTANT: '0' | [1-9][0-9]*;
REAL_CONSTANT: [1-9][0-9]*'.'[0-9]* | '0.'[0-9]*;
IDENTIFIER: ('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')*;


ADD_ASSIGN:  '+=';
SUB_ASSIGN:  '-=';
MUL_ASSIGN:  '*=';
DIV_ASSIGN:  '/=';
MOD_ASSIGN:  '%=';
INC_OP:  '++';
DEC_OP:  '--';
AND_OP:  '&&';
OR_OP:  '||';
LE_OP:  '<=';
GE_OP:  '>=';
EQ_OP:  '==';
NE_OP:  '!=';
SEMICOLON: ';';
LEFTBRACE: '{';
RIGHTBRACE: '}';
COMMA: ',';
COLON: ':';
ASSIGN: '=';
LEFTPARENTHESIS: '(';
RIGHTPARENTHESIS: ')';
LEFTSQUAREBRACKET: '[';
RIGHTSQUAREBRACKET: ']';
NOT: '!';
MINUS: '-';
PLUS: '+';
MUL: '*';
DIV: '/';
MOD: '%';
LESSTHAN: '<';
GREATERTHAN: '>';
BEGININLINECOMMENT: '//';
BEGINCOMMENT: '/*';
ENDCOMMENT: '*/';