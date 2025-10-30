parser grammar RPLParser;
options { tokenVocab=RPLLexer; }


program
    : statement* EOF
    ;

statement
    : roleDeclaration
    | userDeclaration
    | resourceDeclaration
    | policyRule
    ;

// Role declarations: ROLE Admin {can: *}
roleDeclaration
    : ROLE IDENTIFIER LBRACE rolePermissions RBRACE
    ;

rolePermissions
    : CAN COLON permission (COMMA permission)*
    ;


// User declarations: USER JaneDoe {role: Developer}
userDeclaration
    : USER IDENTIFIER LBRACE userAttributes RBRACE
    ;

userAttributes
    : userAssignment COLON userAttribute
    |
    ;

userAttribute
    : IDENTIFIER (COMMA userAttribute)*
    ;

userAssignment
    : ROLE
    ;

// Resource declarations: RESOURCE DB_Finance {path: /data/financial}
resourceDeclaration
    : RESOURCE IDENTIFIER LBRACE resourceAttributes RBRACE
    ;

resourceAttributes
    : resourceAttribute (COMMA resourceAttribute)*
    ;

resourceAttribute
    : IDENTIFIER COLON value
    ;

// Policy rules: ALLOW/DENY action ON resource IF condition
policyRule
    : policyType ACTION COLON actionList ON RESOURCE COLON resourceRef ifClause?
    ;

policyType
    : ALLOW
    | DENY
    ;

actionList
    : permission (COMMA permission)*
    ;


permission
    : READ
    | WRITE
    | MODIFY
    | START
    | STOP
    | DEPLOY
    | DELETE
    | EXECUTE
    | STAR  // Wildcard for all permissions
    ;

resourceRef
    : IDENTIFIER
    | STRING
    ;

ifClause
    : IF LPAREN condition RPAREN    # parenCondition
    ;

// Conditions with Boolean logic
condition
    : condition AND condition           # andCondition
    | condition OR condition            # orCondition
    | NOT condition                     # notCondition
    | comparison                        # comparisonCondition
    ;

comparison
    : expression comparisonOp expression
    ;

comparisonOp
    : EQ | NE | LT | GT | LE | GE
    ;


expression
    : expression op=(STAR | DIV) expression       # multiDiv
    | expression op=(PLUS | MINUS) expression     # addSub
    | LPAREN expression RPAREN                    # parenExpr
    | INTEGER                                     # integer
    | REAL                                        # float
    | IDENTIFIER                                  # identifier
    | memberAccess                                # memberExpr
    ;


memberAccess
    : IDENTIFIER DOT ROLE
    | IDENTIFIER DOT IDENTIFIER
    ;

value
    : STRING
    | CHARACTER
    | INTEGER
    | REAL
    | IDENTIFIER
    | BOOLEAN
    ;