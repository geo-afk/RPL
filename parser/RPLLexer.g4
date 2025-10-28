lexer grammar RPLLexer;


ROLE        : ([Rr][Oo][Ll][Ee]);
USER        : [Uu][Ss][Ee][Rr];
RESOURCE    : [Rr][Ee][Ss][Oo][Uu][Rr][Cc][Ee] ;
ALLOW       : [Aa][Ll][Ll][Oo][Ww] ;
DENY        : [Dd][Ee][Nn][Yy] ;
ACTION      : [Aa][Cc][Tt][Ii][Oo][Nn] ;
READ        : [Rr][Ee][Aa][Dd] ;
WRITE       : [Ww][Rr][Ii][Tt][Ee] ;
MODIFY      : [Mm][Oo][Dd][Ii][Ff][Yy] ;
START       : [Ss][Tt][Aa][Rr][Tt] ;
STOP        : [Ss][Tt][Oo][Pp] ;
DEPLOY      : [Dd][Ee][Pp][Ll][Oo][Yy] ;
DELETE      : [Dd][Ee][Ll][Ee][Tt][Ee] ;
EXECUTE     : [Ee][Xx][Ee][Cc][Uu][Tt][Ee] ;
POLICYTYPE  : ALLOW | DENY ;
ON          : [Oo][Nn] ;
IF          : [Ii][Ff] ;
AND         : [Aa][Nn][Dd] ;
OR          : [Oo][Rr] ;
NOT         : [Nn][Oo][Tt] ;
CAN         : [Cc][Aa][Nn] ;

// Operators
EQ          : '==';
NE          : '!=';
LT          : '<';
GT          : '>';
LE          : '<=';
GE          : '>=';
PLUS        : '+';
MINUS       : '-';
DIV         : '/';
STAR        : '*';  

// Delimiters
LPAREN      : '(';
RPAREN      : ')';
LBRACE      : '{';
RBRACE      : '}';
COLON       : ':';
SEMICOLON   : ';';
COMMA       : ',';
DOT         : '.';


fragment DIGIT: [0-9] ;
fragment ESCAPE_SEQUENCE:
    '\\\''
    | '\\"'
    | '\\\\'
    | '\\n'
    | '\\r'
    | '\\' ('\r' '\n'? | '\n')
;

// Literals
BOOLEAN     : 'true' | 'false';
INTEGER: DIGIT+ ;
REAL: DIGIT+ '.' DIGIT* | '.' DIGIT+;
STRING: '"' (~["\r\n] | ESCAPE_SEQUENCE)* '"' ;
CHARACTER: '\'' (~['\r\n] | ESCAPE_SEQUENCE) '\'' ;

// Identifiers (must come after keywords)
IDENTIFIER  : [a-zA-Z_][a-zA-Z0-9_]*;

// Whitespace and comments
WS          : [ \t\r\n]+ -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;