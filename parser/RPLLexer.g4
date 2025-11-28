lexer grammar RPLLexer;

// Keywords
ROLE : [Rr][Oo][Ll][Ee];
USER : [Uu][Ss][Ee][Rr];
RESOURCE : [Rr][Ee][Ss][Oo][Uu][Rr][Cc][Ee];
CAN : [Cc][Aa][Nn];
EXTENDS : [Ee][Xx][Tt][Ee][Nn][Dd][Ss];
PERMISSIONS : [Pp][Ee][Rr][Mm][Ii][Ss][Ss][Ii][Oo][Nn][Ss];
ACTIONS : [Aa][Cc][Tt][Ii][Oo][Nn][Ss];
RESOURCES : [Rr][Ee][Ss][Oo][Uu][Rr][Cc][Ee][Ss];
CONDITIONS : [Cc][Oo][Nn][Dd][Ii][Tt][Ii][Oo][Nn][Ss];
GROUP : [Gg][Rr][Oo][Uu][Pp];
MEMBERS : [Mm][Ee][Mm][Bb][Ee][Rr][Ss];
VALID_FROM : [Vv][Aa][Ll][Ii][Dd][_][Ff][Rr][Oo][Mm];
VALID_UNTIL : [Vv][Aa][Ll][Ii][Dd][_][Uu][Nn][Tt][Ii][Ll];

// Resource-specific keywords
PATH : [Pp][Aa][Tt][Hh];
TYPE : [Tt][Yy][Pp][Ee];
METADATA : [Mm][Ee][Tt][Aa][Dd][Aa][Tt][Aa];

// Resource type literals
API : [Aa][Pp][Ii];
FOLDER : [Ff][Oo][Ll][Dd][Ee][Rr];
DATABASE : [Dd][Aa][Tt][Aa][Bb][Aa][Ss][Ee];

// Logical operators
AND : [Aa][Nn][Dd];
OR : [Oo][Rr];
NOT : [Nn][Oo][Tt];

// Action keywords
READ : [Rr][Ee][Aa][Dd];
WRITE : [Ww][Rr][Ii][Tt][Ee];
MODIFY : [Mm][Oo][Dd][Ii][Ff][Yy];
START : [Ss][Tt][Aa][Rr][Tt];
STOP : [Ss][Tt][Oo][Pp];
DEPLOY : [Dd][Ee][Pp][Ll][Oo][Yy];
DELETE : [Dd][Ee][Ll][Ee][Tt][Ee];
EXECUTE : [Ee][Xx][Ee][Cc][Uu][Tt][Ee];

// Special symbols
STAR : '*';

// Comparison operators
EQ : '==';
NE : '!=';
LT : '<';
GT : '>';
LE : '<=';
GE : '>=';
PLUS : '+';
MINUS : '-';
DIV : '/';
IN : [Ii][Nn];
CONTAINS : [Cc][Oo][Nn][Tt][Aa][Ii][Nn][Ss];

// Delimiters
LBRACKET : '[';
RBRACKET : ']';
LPAREN : '(';
RPAREN : ')';
LBRACE : '{';
RBRACE : '}';
COLON : ':';
COMMA : ',';
DOT : '.';

// Literals
BOOLEAN : 'true' | 'false';
INTEGER : [0-9]+;
REAL : [0-9]+ '.' [0-9]* | '.' [0-9]+;
STRING : '"' (~["\r\n] | '\\' . )* '"' ;
CHARACTER : '\'' (~['\r\n] | '\\' . ) '\'' ;

IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]*;

// Whitespace and comments
WS : [ \t\r\n]+ -> skip;
LINE_COMMENT : '//' ~[\r\n]* -> skip;
BLOCK_COMMENT : '/*' .*? '*/' -> skip;