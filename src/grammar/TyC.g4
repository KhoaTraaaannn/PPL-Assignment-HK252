grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// --- PARSER --- //

// TODO Literal Integer, floating-point, and string literals

literal
    : INT_LITERAL
    | FLOAT_LITERAL
    | STRING_LITERAL
    ;

expression
    : assignment_expression
    ;

assignment_expression
    : assign_lhs ASS assignment_expression
    | logical_or_expression
    ;


logical_or_expression
    : logical_and_expression (OR logical_and_expression)*
    ;

logical_and_expression
    : equality_expression (AND equality_expression)*
    ;

equality_expression
    : relational_expression ((EQ | NE) relational_expression)*
    ;

relational_expression
    : additive_expression ((LT | LE | GT | GE) additive_expression)*
    ;

additive_expression
    : multiplicative_expression ((ADD | SUB) multiplicative_expression)*
    ;

multiplicative_expression
    : unary_expression ((MUL | DIV | MOD) unary_expression)*
    ;

unary_expression
    : ADD unary_expression
    | SUB unary_expression
    | NOT unary_expression
    | incdec_expression
    ;

non_prefix_unary
    : incdec_expression
    ;

prefix_incdec
    : INCRE non_prefix_unary
    | DECRE non_prefix_unary
    ;


incdec_expression
    : prefix_incdec postfix_tail
    | postfix_expression
    ;

postfix_tail
    : (INCRE | DECRE)*
    ;


postfix_expression
    : postfix_expression INCRE
    | postfix_expression DECRE
    | primary_postfix
    ;
    
primary_postfix
    : member_access
    | lvalue
    | function_call
    | literal
    | struct_init
    | LP expression RP
    ;

non_call_primary
    : ID
    | literal
    | struct_init
    | LP expression RP
    ;


lvalue
    : ID (MEMACC ID)*
    ;


function_call
    : ID LP argument_list? RP
    ;

primary_expression
    : function_call
    | ID
    | literal
    | struct_init
    | LP expression RP
    ;

argument_list
    : expression (COMMA expression)*
    ;

// TODO type `int`, `float`, `string`, `void`, struct types, and type inference using `auto`
type
    : INT
    | FLOAT
    | STRING
    | ID
    ;

return_type
    : type
    | VOID
    ;

// TODO Statements Variable declarations, assignments, control flow (if, while, for, switch-case), break, continue, return, expression statements, and blocks
statement
    : var_statement SEMI
    | assign_statement SEMI
    | postfix_expression SEMI
    | if_statement
    | while_statement
    | for_statement
    | switch_statement
    | break_statement SEMI
    | continue_statement SEMI
    | return_statement
    | block_statement
    ;


block_statement
    : LB statement* RB
    ;

var_statement
    : AUTO ID (ASS (expression | struct_init))?
    | type ID (ASS (expression | struct_init))?
    ;

assign_statement
    : assignment_expression
    ;

member_base
    : ID
    | function_call
    | literal
    | struct_init
    | LP expression RP
    ;

member_access
    : member_base (MEMACC ID)+
    ;


assign_lhs
    : ID
    | member_access
    ;

if_statement
    : IF LP expression RP statement (ELSE statement)?
    ;

while_statement
    : WHILE LP expression RP statement
    ;

for_statement
    : FOR LP for_init? SEMI
           expression? SEMI
           for_update?
      RP statement
    ;
for_init
    : var_statement
    | assign_lhs ASS assignment_expression
    ;

for_update
    : assign_lhs ASS assignment_expression
    | prefix_incdec
    | postfix_expression INCRE
    | postfix_expression DECRE
    ;

switch_statement
    : SWITCH LP expression RP LB switch_body RB
    ;

switch_body
    : case_clause* default_clause? case_clause*
    ;

case_clause
    : CASE expression COLON statement*
    ;

default_clause
    : DEFAULT COLON statement*
    ;

break_statement
    : BREAK
    ;

continue_statement
    : CONTINUE
    ;

return_statement
    : RETURN (expression | struct_init)? SEMI
    ;

program
    : (struct_decl | function_decl)* EOF
    ;

struct_init
    : LB (expression (COMMA expression)*)? RB
    ;

struct_decl
    : STRUCT ID LB struct_member* RB SEMI
    ;

struct_member
    : type ID SEMI
    ;

function_decl
    : return_type? ID LP param_list? RP block_statement
    ;

param_list
    : param (COMMA param)*
    ;

param
    : type ID
    ;


// --- TODO TASK LEXER --- //
// TODO Keywords
AUTO      : 'auto';
BREAK     : 'break';
CASE      : 'case';
CONTINUE  : 'continue';
DEFAULT   : 'default';
ELSE      : 'else';

FLOAT     : 'float';
FOR       : 'for';
IF        : 'if';
INT       : 'int';
RETURN    : 'return';
STRING    : 'string';

STRUCT    : 'struct';
SWITCH    : 'switch';
VOID      : 'void';
WHILE     : 'while';
// TODO Operator
OR         : '||';
AND        : '&&';
EQ         : '==';
NE         : '!=';
LE         : '<=';
GE         : '>=';
INCRE      : '++';
DECRE      : '--';
ADD        : '+';
SUB        : '-';
MUL        : '*';
DIV        : '/';
MOD        : '%';
LT         : '<';
GT         : '>';
NOT        : '!';
ASS        : '=';
MEMACC     : '.';

// TODO Separator
LB         : '{';
RB         : '}';
LP         : '(';
RP         : ')';
SEMI       : ';';
COMMA      : ',';
COLON      : ':';
// TODO Identifiers

ID
    : [a-zA-Z_][a-zA-Z_0-9]*
    ;


// TODO Literals
INT_LITERAL
    : [0-9]+ { ... }?
      { (self._input.LA(1) == ord('.')) or (self._tokenStartCharIndex > 0 and chr(self._input.data[self._tokenStartCharIndex - 1]) in ('e','E')) }?
    | [0-9]+
    ;

FLOAT_LITERAL
    : [0-9]+ '.' [0-9]+ EXPONENT?
    | [0-9]+ '.' EXPONENT?      
    | '.' [0-9]+ EXPONENT?
    | [0-9]+ EXPONENT
    ;

fragment EXPONENT
    : [eE] [+-]? [0-9]+
    ;

STRING_LITERAL
    : '"' ( ESC_SEQ | ~["\\\r\n] )* '"'
      { self.text = self.text[1:-1] }
    ;

fragment ESC_SEQ
    : '\\' [btnfr"\\]
    ;

// TODO Comment and WS
LINE_COMMENT
    : '//' ~[\r\n]* -> skip
    ;

BLOCK_COMMENT
    : '/*' .*? '*/' -> skip
    ;

WS
    : [ \t\r\n\f]+ -> skip
    ;

// TODO ERROR
UNCLOSE_STRING
    : '"' (ESC_SEQ | ~["\\\r\n])* '\\'? ('\r'? '\n' | EOF)
    {
        txt = self.text[1:]
        if txt.endswith('\r\n'):
            txt = txt[:-2]
        elif txt.endswith('\n') or txt.endswith('\r'):
            txt = txt[:-1]
        raise UncloseString(txt)
    };


ILLEGAL_ESCAPE
    : '"' ( ESC_SEQ | ~["\\\r\n] )* '\\' ~[btnfr"\\]
      { self.text = self.text[1:] }
    ;


ERROR_CHAR
    : .
    ;