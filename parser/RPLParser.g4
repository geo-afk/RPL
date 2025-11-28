parser grammar RPLParser;

options { tokenVocab=RPLLexer; }

program
    : statement* EOF
    ;

statement
    : roleDeclaration
    | userDeclaration
    | resourceDeclaration
    | groupDeclaration
    ;

roleDeclaration
    : ROLE IDENTIFIER (EXTENDS IDENTIFIER)? LBRACE roleBody RBRACE
    ;

roleBody
    : rolePermissions+
    ;

rolePermissions
    : PERMISSIONS COLON LBRACKET permissionBlock (COMMA permissionBlock)* RBRACKET
    | CAN COLON LBRACKET permission (COMMA permission)* RBRACKET RESOURCES COLON LBRACKET resourceList RBRACKET
    ;

permissionBlock
    : LBRACE
        ACTIONS COLON LBRACKET actionList RBRACKET COMMA
        RESOURCES COLON LBRACKET resourceList RBRACKET
        (COMMA CONDITIONS COLON condition)?
      RBRACE
    ;

userDeclaration
    : USER IDENTIFIER LBRACE userBody RBRACE
    ;

userBody
    : userRoles?
    | userRoles? COMMA validPeriod
    | validPeriod
    ;

validPeriod
    : validFrom COMMA validUntil
    ;

userRoles
    : ROLE COLON LBRACKET IDENTIFIER (COMMA IDENTIFIER)* RBRACKET
    ;

validFrom  : VALID_FROM  COLON STRING ;
validUntil : VALID_UNTIL COLON STRING ;

// Enhanced resource declaration with path, type, and metadata
resourceDeclaration
    : RESOURCE IDENTIFIER LBRACE resourceBody RBRACE
    ;

resourceBody
    : resourceProperty (COMMA resourceProperty)*
    ;

resourceProperty
    : PATH COLON STRING
    | TYPE COLON resourceType
    | METADATA COLON metadataBlock
//    | IDENTIFIER COLON value  // Allow other custom properties for backward compatibility
    ;

resourceType
    : API
    | FOLDER
    | DATABASE
    ;

// Metadata as structured key-value pairs
metadataBlock
    : LBRACE metadataEntry (COMMA metadataEntry)* RBRACE
    | LBRACE RBRACE  // Allow empty metadata
    ;

metadataEntry
    : IDENTIFIER COLON value
    ;

resourceList
    : resourceRef (COMMA resourceRef)*
    ;

resourceRef
    : IDENTIFIER (DOT (IDENTIFIER | STAR))*
    | STRING
    ;

groupDeclaration
    : GROUP IDENTIFIER LBRACE groupBody RBRACE
    ;

groupBody
    : (groupMembers? (COMMA groupRoles?)? )
    ;

groupMembers
    : MEMBERS COLON LBRACKET memberList RBRACKET
    ;

memberList
    : IDENTIFIER (COMMA IDENTIFIER)*
    ;

groupRoles
    : ROLE COLON LBRACKET IDENTIFIER (COMMA IDENTIFIER)* RBRACKET
    ;

actionList
    : permission (COMMA permission)*
    ;

permission
    : READ | WRITE | MODIFY | START | STOP | DEPLOY | DELETE | EXECUTE | STAR
    ;

condition
    : orCondition
    ;

orCondition
    : andCondition (OR andCondition)*
    ;

andCondition
    : notCondition (AND notCondition)*
    ;

notCondition
    : NOT notCondition
    | primaryCondition
    ;

primaryCondition
    : LPAREN condition RPAREN
    | comparison
    ;

comparison
    : expression comparisonOp expression
    | expression IN LBRACKET valueList RBRACKET
    | expression CONTAINS value
    ;

comparisonOp
    : EQ | NE | LT | GT | LE | GE
    ;

expression
    : additiveExpr
    ;

additiveExpr
    : multiplicativeExpr ((PLUS | MINUS) multiplicativeExpr)*
    ;

multiplicativeExpr
    : unaryExpr ((STAR | DIV) unaryExpr)*
    ;

unaryExpr
    : PLUS unaryExpr
    | MINUS unaryExpr
    | primaryExpr
    ;

primaryExpr
    : LPAREN expression RPAREN
    | atom
    ;

atom
    : INTEGER
    | REAL
    | STRING
    | BOOLEAN
    | qualifiedName
    ;

qualifiedName
    : IDENTIFIER (DOT IDENTIFIER)*
    ;

value
    : STRING
    | CHARACTER
    | INTEGER
    | REAL
    | IDENTIFIER
    | BOOLEAN
    | LBRACKET valueList RBRACKET
    ;

valueList
    : value (COMMA value)*
    ;