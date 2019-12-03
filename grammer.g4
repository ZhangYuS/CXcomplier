grammar grammer;
r   :
    translation_unit
    ;

translation_unit
    : external_declaration
    | translation_unit external_declaration
    ;

external_declaration
    : function_definition
    ;

function_definition
    : declaration_specifiers declarator block
    ;

block
    : '{' '}'
    | '{' compound_statement '}'
    ;

declaration_specifiers
    : type_specifier
    ;

type_specifier
    : VOID
    | INT
    | BOOL
    ;

declarator
    : IDENTIFIER
    | declarator '[' constant_expression ']'
    | declarator '(' parameter_list ')'
    | declarator '(' identifier_list ')'
    | declarator '(' ')'
    ;

constant_expression
    : logical_and_expression
    ;

parameter_list
    : parameter_list ',' parameter_declaration
    | parameter_declaration
    ;

parameter_declaration
    : declaration_specifiers declarator
    ;

identifier_list
    : IDENTIFIER
    | identifier_list ',' IDENTIFIER
    ;

compound_statement
    : compound_statement declaration_list
    | compound_statement statement_list
    | declaration_list
    | statement_list
    ;

declaration_list
    : declaration
    | declaration_list declaration
    ;

declaration
    : declaration_specifiers ';'
    | declaration_specifiers init_declarator_list ';'
    ;

init_declarator_list
    : init_declarator
    | init_declarator_list ',' init_declarator
    ;

init_declarator
    : declarator
    | declarator '=' initializer
    ;

initializer
    : assignment_expression
    ;

statement_list
    : statement
    | statement_list statement
    ;

statement
    : expression_statement
    | output_statement
    ;

expression_statement
    : expression ';'
    | ';'
    ;

expression
    : assignment_expression
    | expression ',' assignment_expression
    ;

assignment_expression
    : logical_or_expression
    | unary_expression assignment_operator assignment_expression
    ;

assignment_operator
    : '='
    | MUL_ASSIGN
    | DIV_ASSIGN
    | MOD_ASSIGN
    | ADD_ASSIGN
    | SUB_ASSIGN
    | AND_ASSIGN
    | OR_ASSIGN
    ;

logical_or_expression
    : logical_and_expression
    | logical_or_expression OR_OP logical_and_expression
    ;

logical_and_expression
    : and_expression
    | logical_and_expression AND_OP and_expression
    ;

and_expression
    : equality_expression
    | and_expression '&' equality_expression
    ;

equality_expression
    : relational_expression
    | equality_expression EQ_OP relational_expression
    | equality_expression NE_OP relational_expression
    ;

relational_expression
    : additive_expression
    | relational_expression '<' additive_expression
    | relational_expression '>' additive_expression
    | relational_expression LE_OP additive_expression
    | relational_expression GE_OP additive_expression
    ;

additive_expression
    : multiplicative_expression
    | additive_expression '+' multiplicative_expression
    | additive_expression '-' multiplicative_expression
    ;

multiplicative_expression
    : unary_expression
    | multiplicative_expression '*' unary_expression
    | multiplicative_expression '/' unary_expression
    | multiplicative_expression '%' unary_expression
    ;

unary_expression
    : postfix_expression
    | INC_OP unary_expression
    | DEC_OP unary_expression
    | unary_operator multiplicative_expression
    ;

unary_operator
    : '&'
    | '*'
    | '+'
    | '-'
    | '~'
    | '!'
    ;

postfix_expression
    : primary_expression
    | postfix_expression '[' expression ']'
    | postfix_expression '(' ')'
    | postfix_expression '(' argument_expression_list ')'
    | postfix_expression INC_OP
    | postfix_expression DEC_OP
    ;

argument_expression_list
    : assignment_expression
    | argument_expression_list ',' assignment_expression
    ;

primary_expression
    : IDENTIFIER
    | INT_CONSTANT
    | BOOL_CONSTANT
    | REAL_CONSTANT
    | '(' expression ')'
    ;

output_statement
    : OUTPUT expression_statement
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
VOID: 'void';
WHILE: 'while';
BOOL: 'bool';
REAL: 'real';
BOOL_CONSTANT: 'true' | 'false';
OUTPUT: 'write';


INT_CONSTANT: '0' | [1-9][0-9]*;
REAL_CONSTANT: [1-9][0-9]*'.'[0-9]* | '0.'[0-9]*;
IDENTIFIER: ('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')*;


ADD_ASSIGN:  '+= ';
SUB_ASSIGN:  '-= ';
MUL_ASSIGN:  '*= ';
DIV_ASSIGN:  '/= ';
MOD_ASSIGN:  '%= ';
INC_OP:  '++ ';
DEC_OP:  '-- ';
AND_OP:  '&& ';
OR_OP:  '|| ';
LE_OP:  '<= ';
GE_OP:  '>= ';
EQ_OP:  '== ';
NE_OP:  '!= ';
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


[ \t\v\n\f]  { }
.    { /* ignore bad characters */ }