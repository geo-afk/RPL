# Generated from RPLParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,48,203,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,1,0,5,0,48,8,0,10,0,12,0,51,9,0,1,0,1,0,
        1,1,1,1,1,1,1,1,3,1,59,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,1,
        3,1,3,5,3,72,8,3,10,3,12,3,75,9,3,1,4,1,4,1,4,1,4,1,4,1,4,1,5,1,
        5,1,5,1,5,1,5,3,5,88,8,5,1,6,1,6,1,6,5,6,93,8,6,10,6,12,6,96,9,6,
        1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,9,1,9,1,9,5,9,109,8,9,10,9,12,
        9,112,9,9,1,10,1,10,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,11,1,11,
        1,11,1,11,3,11,127,8,11,1,12,1,12,1,13,1,13,1,13,5,13,134,8,13,10,
        13,12,13,137,9,13,1,14,1,14,1,15,1,15,1,16,1,16,1,16,1,16,1,16,1,
        17,1,17,1,17,1,17,3,17,152,8,17,1,17,1,17,1,17,1,17,1,17,1,17,5,
        17,160,8,17,10,17,12,17,163,9,17,1,18,1,18,1,18,1,18,1,19,1,19,1,
        20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,3,20,180,8,20,1,20,1,
        20,1,20,1,20,1,20,1,20,5,20,188,8,20,10,20,12,20,191,9,20,1,21,1,
        21,1,21,1,21,1,21,1,21,3,21,199,8,21,1,22,1,22,1,22,0,2,34,40,23,
        0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,
        0,7,1,0,4,5,2,0,7,14,31,31,2,0,43,43,45,45,1,0,22,27,1,0,30,31,1,
        0,28,29,1,0,40,45,199,0,49,1,0,0,0,2,58,1,0,0,0,4,60,1,0,0,0,6,66,
        1,0,0,0,8,76,1,0,0,0,10,87,1,0,0,0,12,89,1,0,0,0,14,97,1,0,0,0,16,
        99,1,0,0,0,18,105,1,0,0,0,20,113,1,0,0,0,22,117,1,0,0,0,24,128,1,
        0,0,0,26,130,1,0,0,0,28,138,1,0,0,0,30,140,1,0,0,0,32,142,1,0,0,
        0,34,151,1,0,0,0,36,164,1,0,0,0,38,168,1,0,0,0,40,179,1,0,0,0,42,
        198,1,0,0,0,44,200,1,0,0,0,46,48,3,2,1,0,47,46,1,0,0,0,48,51,1,0,
        0,0,49,47,1,0,0,0,49,50,1,0,0,0,50,52,1,0,0,0,51,49,1,0,0,0,52,53,
        5,0,0,1,53,1,1,0,0,0,54,59,3,4,2,0,55,59,3,8,4,0,56,59,3,16,8,0,
        57,59,3,22,11,0,58,54,1,0,0,0,58,55,1,0,0,0,58,56,1,0,0,0,58,57,
        1,0,0,0,59,3,1,0,0,0,60,61,5,1,0,0,61,62,5,45,0,0,62,63,5,34,0,0,
        63,64,3,6,3,0,64,65,5,35,0,0,65,5,1,0,0,0,66,67,5,21,0,0,67,68,5,
        36,0,0,68,73,3,28,14,0,69,70,5,38,0,0,70,72,3,28,14,0,71,69,1,0,
        0,0,72,75,1,0,0,0,73,71,1,0,0,0,73,74,1,0,0,0,74,7,1,0,0,0,75,73,
        1,0,0,0,76,77,5,2,0,0,77,78,5,45,0,0,78,79,5,34,0,0,79,80,3,10,5,
        0,80,81,5,35,0,0,81,9,1,0,0,0,82,83,3,14,7,0,83,84,5,36,0,0,84,85,
        3,12,6,0,85,88,1,0,0,0,86,88,1,0,0,0,87,82,1,0,0,0,87,86,1,0,0,0,
        88,11,1,0,0,0,89,94,5,45,0,0,90,91,5,38,0,0,91,93,3,12,6,0,92,90,
        1,0,0,0,93,96,1,0,0,0,94,92,1,0,0,0,94,95,1,0,0,0,95,13,1,0,0,0,
        96,94,1,0,0,0,97,98,5,1,0,0,98,15,1,0,0,0,99,100,5,3,0,0,100,101,
        5,45,0,0,101,102,5,34,0,0,102,103,3,18,9,0,103,104,5,35,0,0,104,
        17,1,0,0,0,105,110,3,20,10,0,106,107,5,38,0,0,107,109,3,20,10,0,
        108,106,1,0,0,0,109,112,1,0,0,0,110,108,1,0,0,0,110,111,1,0,0,0,
        111,19,1,0,0,0,112,110,1,0,0,0,113,114,5,45,0,0,114,115,5,36,0,0,
        115,116,3,44,22,0,116,21,1,0,0,0,117,118,3,24,12,0,118,119,5,6,0,
        0,119,120,5,36,0,0,120,121,3,26,13,0,121,122,5,16,0,0,122,123,5,
        3,0,0,123,124,5,36,0,0,124,126,3,30,15,0,125,127,3,32,16,0,126,125,
        1,0,0,0,126,127,1,0,0,0,127,23,1,0,0,0,128,129,7,0,0,0,129,25,1,
        0,0,0,130,135,3,28,14,0,131,132,5,38,0,0,132,134,3,28,14,0,133,131,
        1,0,0,0,134,137,1,0,0,0,135,133,1,0,0,0,135,136,1,0,0,0,136,27,1,
        0,0,0,137,135,1,0,0,0,138,139,7,1,0,0,139,29,1,0,0,0,140,141,7,2,
        0,0,141,31,1,0,0,0,142,143,5,17,0,0,143,144,5,32,0,0,144,145,3,34,
        17,0,145,146,5,33,0,0,146,33,1,0,0,0,147,148,6,17,-1,0,148,149,5,
        20,0,0,149,152,3,34,17,2,150,152,3,36,18,0,151,147,1,0,0,0,151,150,
        1,0,0,0,152,161,1,0,0,0,153,154,10,4,0,0,154,155,5,18,0,0,155,160,
        3,34,17,5,156,157,10,3,0,0,157,158,5,19,0,0,158,160,3,34,17,4,159,
        153,1,0,0,0,159,156,1,0,0,0,160,163,1,0,0,0,161,159,1,0,0,0,161,
        162,1,0,0,0,162,35,1,0,0,0,163,161,1,0,0,0,164,165,3,40,20,0,165,
        166,3,38,19,0,166,167,3,40,20,0,167,37,1,0,0,0,168,169,7,3,0,0,169,
        39,1,0,0,0,170,171,6,20,-1,0,171,172,5,32,0,0,172,173,3,40,20,0,
        173,174,5,33,0,0,174,180,1,0,0,0,175,180,5,41,0,0,176,180,5,42,0,
        0,177,180,5,45,0,0,178,180,3,42,21,0,179,170,1,0,0,0,179,175,1,0,
        0,0,179,176,1,0,0,0,179,177,1,0,0,0,179,178,1,0,0,0,180,189,1,0,
        0,0,181,182,10,7,0,0,182,183,7,4,0,0,183,188,3,40,20,8,184,185,10,
        6,0,0,185,186,7,5,0,0,186,188,3,40,20,7,187,181,1,0,0,0,187,184,
        1,0,0,0,188,191,1,0,0,0,189,187,1,0,0,0,189,190,1,0,0,0,190,41,1,
        0,0,0,191,189,1,0,0,0,192,193,5,45,0,0,193,194,5,39,0,0,194,199,
        5,1,0,0,195,196,5,45,0,0,196,197,5,39,0,0,197,199,5,45,0,0,198,192,
        1,0,0,0,198,195,1,0,0,0,199,43,1,0,0,0,200,201,7,6,0,0,201,45,1,
        0,0,0,15,49,58,73,87,94,110,126,135,151,159,161,179,187,189,198
    ]

class RPLParser ( Parser ):

    grammarFileName = "RPLParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'=='", "'!='", "'<'", "'>'", 
                     "'<='", "'>='", "'+'", "'-'", "'/'", "'*'", "'('", 
                     "')'", "'{'", "'}'", "':'", "';'", "','", "'.'" ]

    symbolicNames = [ "<INVALID>", "ROLE", "USER", "RESOURCE", "ALLOW", 
                      "DENY", "ACTION", "READ", "WRITE", "MODIFY", "START", 
                      "STOP", "DEPLOY", "DELETE", "EXECUTE", "POLICYTYPE", 
                      "ON", "IF", "AND", "OR", "NOT", "CAN", "EQ", "NE", 
                      "LT", "GT", "LE", "GE", "PLUS", "MINUS", "DIV", "STAR", 
                      "LPAREN", "RPAREN", "LBRACE", "RBRACE", "COLON", "SEMICOLON", 
                      "COMMA", "DOT", "BOOLEAN", "INTEGER", "REAL", "STRING", 
                      "CHARACTER", "IDENTIFIER", "WS", "LINE_COMMENT", "BLOCK_COMMENT" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_roleDeclaration = 2
    RULE_rolePermissions = 3
    RULE_userDeclaration = 4
    RULE_userAttributes = 5
    RULE_userAttribute = 6
    RULE_userAssignment = 7
    RULE_resourceDeclaration = 8
    RULE_resourceAttributes = 9
    RULE_resourceAttribute = 10
    RULE_policyRule = 11
    RULE_policyType = 12
    RULE_actionList = 13
    RULE_permission = 14
    RULE_resourceRef = 15
    RULE_ifClause = 16
    RULE_condition = 17
    RULE_comparison = 18
    RULE_comparisonOp = 19
    RULE_expression = 20
    RULE_memberAccess = 21
    RULE_value = 22

    ruleNames =  [ "program", "statement", "roleDeclaration", "rolePermissions", 
                   "userDeclaration", "userAttributes", "userAttribute", 
                   "userAssignment", "resourceDeclaration", "resourceAttributes", 
                   "resourceAttribute", "policyRule", "policyType", "actionList", 
                   "permission", "resourceRef", "ifClause", "condition", 
                   "comparison", "comparisonOp", "expression", "memberAccess", 
                   "value" ]

    EOF = Token.EOF
    ROLE=1
    USER=2
    RESOURCE=3
    ALLOW=4
    DENY=5
    ACTION=6
    READ=7
    WRITE=8
    MODIFY=9
    START=10
    STOP=11
    DEPLOY=12
    DELETE=13
    EXECUTE=14
    POLICYTYPE=15
    ON=16
    IF=17
    AND=18
    OR=19
    NOT=20
    CAN=21
    EQ=22
    NE=23
    LT=24
    GT=25
    LE=26
    GE=27
    PLUS=28
    MINUS=29
    DIV=30
    STAR=31
    LPAREN=32
    RPAREN=33
    LBRACE=34
    RBRACE=35
    COLON=36
    SEMICOLON=37
    COMMA=38
    DOT=39
    BOOLEAN=40
    INTEGER=41
    REAL=42
    STRING=43
    CHARACTER=44
    IDENTIFIER=45
    WS=46
    LINE_COMMENT=47
    BLOCK_COMMENT=48

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(RPLParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RPLParser.StatementContext)
            else:
                return self.getTypedRuleContext(RPLParser.StatementContext,i)


        def getRuleIndex(self):
            return RPLParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = RPLParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 62) != 0):
                self.state = 46
                self.statement()
                self.state = 51
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 52
            self.match(RPLParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def roleDeclaration(self):
            return self.getTypedRuleContext(RPLParser.RoleDeclarationContext,0)


        def userDeclaration(self):
            return self.getTypedRuleContext(RPLParser.UserDeclarationContext,0)


        def resourceDeclaration(self):
            return self.getTypedRuleContext(RPLParser.ResourceDeclarationContext,0)


        def policyRule(self):
            return self.getTypedRuleContext(RPLParser.PolicyRuleContext,0)


        def getRuleIndex(self):
            return RPLParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = RPLParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 58
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 54
                self.roleDeclaration()
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 55
                self.userDeclaration()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 3)
                self.state = 56
                self.resourceDeclaration()
                pass
            elif token in [4, 5]:
                self.enterOuterAlt(localctx, 4)
                self.state = 57
                self.policyRule()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RoleDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ROLE(self):
            return self.getToken(RPLParser.ROLE, 0)

        def IDENTIFIER(self):
            return self.getToken(RPLParser.IDENTIFIER, 0)

        def LBRACE(self):
            return self.getToken(RPLParser.LBRACE, 0)

        def rolePermissions(self):
            return self.getTypedRuleContext(RPLParser.RolePermissionsContext,0)


        def RBRACE(self):
            return self.getToken(RPLParser.RBRACE, 0)

        def getRuleIndex(self):
            return RPLParser.RULE_roleDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoleDeclaration" ):
                listener.enterRoleDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoleDeclaration" ):
                listener.exitRoleDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoleDeclaration" ):
                return visitor.visitRoleDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def roleDeclaration(self):

        localctx = RPLParser.RoleDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_roleDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.match(RPLParser.ROLE)
            self.state = 61
            self.match(RPLParser.IDENTIFIER)
            self.state = 62
            self.match(RPLParser.LBRACE)
            self.state = 63
            self.rolePermissions()
            self.state = 64
            self.match(RPLParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RolePermissionsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CAN(self):
            return self.getToken(RPLParser.CAN, 0)

        def COLON(self):
            return self.getToken(RPLParser.COLON, 0)

        def permission(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RPLParser.PermissionContext)
            else:
                return self.getTypedRuleContext(RPLParser.PermissionContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(RPLParser.COMMA)
            else:
                return self.getToken(RPLParser.COMMA, i)

        def getRuleIndex(self):
            return RPLParser.RULE_rolePermissions

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRolePermissions" ):
                listener.enterRolePermissions(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRolePermissions" ):
                listener.exitRolePermissions(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRolePermissions" ):
                return visitor.visitRolePermissions(self)
            else:
                return visitor.visitChildren(self)




    def rolePermissions(self):

        localctx = RPLParser.RolePermissionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_rolePermissions)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.match(RPLParser.CAN)
            self.state = 67
            self.match(RPLParser.COLON)
            self.state = 68
            self.permission()
            self.state = 73
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 69
                self.match(RPLParser.COMMA)
                self.state = 70
                self.permission()
                self.state = 75
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UserDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def USER(self):
            return self.getToken(RPLParser.USER, 0)

        def IDENTIFIER(self):
            return self.getToken(RPLParser.IDENTIFIER, 0)

        def LBRACE(self):
            return self.getToken(RPLParser.LBRACE, 0)

        def userAttributes(self):
            return self.getTypedRuleContext(RPLParser.UserAttributesContext,0)


        def RBRACE(self):
            return self.getToken(RPLParser.RBRACE, 0)

        def getRuleIndex(self):
            return RPLParser.RULE_userDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUserDeclaration" ):
                listener.enterUserDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUserDeclaration" ):
                listener.exitUserDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUserDeclaration" ):
                return visitor.visitUserDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def userDeclaration(self):

        localctx = RPLParser.UserDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_userDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self.match(RPLParser.USER)
            self.state = 77
            self.match(RPLParser.IDENTIFIER)
            self.state = 78
            self.match(RPLParser.LBRACE)
            self.state = 79
            self.userAttributes()
            self.state = 80
            self.match(RPLParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UserAttributesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def userAssignment(self):
            return self.getTypedRuleContext(RPLParser.UserAssignmentContext,0)


        def COLON(self):
            return self.getToken(RPLParser.COLON, 0)

        def userAttribute(self):
            return self.getTypedRuleContext(RPLParser.UserAttributeContext,0)


        def getRuleIndex(self):
            return RPLParser.RULE_userAttributes

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUserAttributes" ):
                listener.enterUserAttributes(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUserAttributes" ):
                listener.exitUserAttributes(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUserAttributes" ):
                return visitor.visitUserAttributes(self)
            else:
                return visitor.visitChildren(self)




    def userAttributes(self):

        localctx = RPLParser.UserAttributesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_userAttributes)
        try:
            self.state = 87
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 82
                self.userAssignment()
                self.state = 83
                self.match(RPLParser.COLON)
                self.state = 84
                self.userAttribute()
                pass
            elif token in [35]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UserAttributeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(RPLParser.IDENTIFIER, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(RPLParser.COMMA)
            else:
                return self.getToken(RPLParser.COMMA, i)

        def userAttribute(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RPLParser.UserAttributeContext)
            else:
                return self.getTypedRuleContext(RPLParser.UserAttributeContext,i)


        def getRuleIndex(self):
            return RPLParser.RULE_userAttribute

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUserAttribute" ):
                listener.enterUserAttribute(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUserAttribute" ):
                listener.exitUserAttribute(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUserAttribute" ):
                return visitor.visitUserAttribute(self)
            else:
                return visitor.visitChildren(self)




    def userAttribute(self):

        localctx = RPLParser.UserAttributeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_userAttribute)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 89
            self.match(RPLParser.IDENTIFIER)
            self.state = 94
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 90
                    self.match(RPLParser.COMMA)
                    self.state = 91
                    self.userAttribute() 
                self.state = 96
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UserAssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ROLE(self):
            return self.getToken(RPLParser.ROLE, 0)

        def getRuleIndex(self):
            return RPLParser.RULE_userAssignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUserAssignment" ):
                listener.enterUserAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUserAssignment" ):
                listener.exitUserAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUserAssignment" ):
                return visitor.visitUserAssignment(self)
            else:
                return visitor.visitChildren(self)




    def userAssignment(self):

        localctx = RPLParser.UserAssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_userAssignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
            self.match(RPLParser.ROLE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ResourceDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RESOURCE(self):
            return self.getToken(RPLParser.RESOURCE, 0)

        def IDENTIFIER(self):
            return self.getToken(RPLParser.IDENTIFIER, 0)

        def LBRACE(self):
            return self.getToken(RPLParser.LBRACE, 0)

        def resourceAttributes(self):
            return self.getTypedRuleContext(RPLParser.ResourceAttributesContext,0)


        def RBRACE(self):
            return self.getToken(RPLParser.RBRACE, 0)

        def getRuleIndex(self):
            return RPLParser.RULE_resourceDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterResourceDeclaration" ):
                listener.enterResourceDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitResourceDeclaration" ):
                listener.exitResourceDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitResourceDeclaration" ):
                return visitor.visitResourceDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def resourceDeclaration(self):

        localctx = RPLParser.ResourceDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_resourceDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 99
            self.match(RPLParser.RESOURCE)
            self.state = 100
            self.match(RPLParser.IDENTIFIER)
            self.state = 101
            self.match(RPLParser.LBRACE)
            self.state = 102
            self.resourceAttributes()
            self.state = 103
            self.match(RPLParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ResourceAttributesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def resourceAttribute(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RPLParser.ResourceAttributeContext)
            else:
                return self.getTypedRuleContext(RPLParser.ResourceAttributeContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(RPLParser.COMMA)
            else:
                return self.getToken(RPLParser.COMMA, i)

        def getRuleIndex(self):
            return RPLParser.RULE_resourceAttributes

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterResourceAttributes" ):
                listener.enterResourceAttributes(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitResourceAttributes" ):
                listener.exitResourceAttributes(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitResourceAttributes" ):
                return visitor.visitResourceAttributes(self)
            else:
                return visitor.visitChildren(self)




    def resourceAttributes(self):

        localctx = RPLParser.ResourceAttributesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_resourceAttributes)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 105
            self.resourceAttribute()
            self.state = 110
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 106
                self.match(RPLParser.COMMA)
                self.state = 107
                self.resourceAttribute()
                self.state = 112
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ResourceAttributeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(RPLParser.IDENTIFIER, 0)

        def COLON(self):
            return self.getToken(RPLParser.COLON, 0)

        def value(self):
            return self.getTypedRuleContext(RPLParser.ValueContext,0)


        def getRuleIndex(self):
            return RPLParser.RULE_resourceAttribute

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterResourceAttribute" ):
                listener.enterResourceAttribute(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitResourceAttribute" ):
                listener.exitResourceAttribute(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitResourceAttribute" ):
                return visitor.visitResourceAttribute(self)
            else:
                return visitor.visitChildren(self)




    def resourceAttribute(self):

        localctx = RPLParser.ResourceAttributeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_resourceAttribute)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            self.match(RPLParser.IDENTIFIER)
            self.state = 114
            self.match(RPLParser.COLON)
            self.state = 115
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PolicyRuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def policyType(self):
            return self.getTypedRuleContext(RPLParser.PolicyTypeContext,0)


        def ACTION(self):
            return self.getToken(RPLParser.ACTION, 0)

        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(RPLParser.COLON)
            else:
                return self.getToken(RPLParser.COLON, i)

        def actionList(self):
            return self.getTypedRuleContext(RPLParser.ActionListContext,0)


        def ON(self):
            return self.getToken(RPLParser.ON, 0)

        def RESOURCE(self):
            return self.getToken(RPLParser.RESOURCE, 0)

        def resourceRef(self):
            return self.getTypedRuleContext(RPLParser.ResourceRefContext,0)


        def ifClause(self):
            return self.getTypedRuleContext(RPLParser.IfClauseContext,0)


        def getRuleIndex(self):
            return RPLParser.RULE_policyRule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPolicyRule" ):
                listener.enterPolicyRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPolicyRule" ):
                listener.exitPolicyRule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPolicyRule" ):
                return visitor.visitPolicyRule(self)
            else:
                return visitor.visitChildren(self)




    def policyRule(self):

        localctx = RPLParser.PolicyRuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_policyRule)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 117
            self.policyType()
            self.state = 118
            self.match(RPLParser.ACTION)
            self.state = 119
            self.match(RPLParser.COLON)
            self.state = 120
            self.actionList()
            self.state = 121
            self.match(RPLParser.ON)
            self.state = 122
            self.match(RPLParser.RESOURCE)
            self.state = 123
            self.match(RPLParser.COLON)
            self.state = 124
            self.resourceRef()
            self.state = 126
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==17:
                self.state = 125
                self.ifClause()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PolicyTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ALLOW(self):
            return self.getToken(RPLParser.ALLOW, 0)

        def DENY(self):
            return self.getToken(RPLParser.DENY, 0)

        def getRuleIndex(self):
            return RPLParser.RULE_policyType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPolicyType" ):
                listener.enterPolicyType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPolicyType" ):
                listener.exitPolicyType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPolicyType" ):
                return visitor.visitPolicyType(self)
            else:
                return visitor.visitChildren(self)




    def policyType(self):

        localctx = RPLParser.PolicyTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_policyType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 128
            _la = self._input.LA(1)
            if not(_la==4 or _la==5):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ActionListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def permission(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RPLParser.PermissionContext)
            else:
                return self.getTypedRuleContext(RPLParser.PermissionContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(RPLParser.COMMA)
            else:
                return self.getToken(RPLParser.COMMA, i)

        def getRuleIndex(self):
            return RPLParser.RULE_actionList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterActionList" ):
                listener.enterActionList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitActionList" ):
                listener.exitActionList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitActionList" ):
                return visitor.visitActionList(self)
            else:
                return visitor.visitChildren(self)




    def actionList(self):

        localctx = RPLParser.ActionListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_actionList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 130
            self.permission()
            self.state = 135
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 131
                self.match(RPLParser.COMMA)
                self.state = 132
                self.permission()
                self.state = 137
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PermissionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def READ(self):
            return self.getToken(RPLParser.READ, 0)

        def WRITE(self):
            return self.getToken(RPLParser.WRITE, 0)

        def MODIFY(self):
            return self.getToken(RPLParser.MODIFY, 0)

        def START(self):
            return self.getToken(RPLParser.START, 0)

        def STOP(self):
            return self.getToken(RPLParser.STOP, 0)

        def DEPLOY(self):
            return self.getToken(RPLParser.DEPLOY, 0)

        def DELETE(self):
            return self.getToken(RPLParser.DELETE, 0)

        def EXECUTE(self):
            return self.getToken(RPLParser.EXECUTE, 0)

        def STAR(self):
            return self.getToken(RPLParser.STAR, 0)

        def getRuleIndex(self):
            return RPLParser.RULE_permission

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPermission" ):
                listener.enterPermission(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPermission" ):
                listener.exitPermission(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPermission" ):
                return visitor.visitPermission(self)
            else:
                return visitor.visitChildren(self)




    def permission(self):

        localctx = RPLParser.PermissionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_permission)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2147516288) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ResourceRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(RPLParser.IDENTIFIER, 0)

        def STRING(self):
            return self.getToken(RPLParser.STRING, 0)

        def getRuleIndex(self):
            return RPLParser.RULE_resourceRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterResourceRef" ):
                listener.enterResourceRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitResourceRef" ):
                listener.exitResourceRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitResourceRef" ):
                return visitor.visitResourceRef(self)
            else:
                return visitor.visitChildren(self)




    def resourceRef(self):

        localctx = RPLParser.ResourceRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_resourceRef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            _la = self._input.LA(1)
            if not(_la==43 or _la==45):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return RPLParser.RULE_ifClause

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ParenConditionContext(IfClauseContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RPLParser.IfClauseContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IF(self):
            return self.getToken(RPLParser.IF, 0)
        def LPAREN(self):
            return self.getToken(RPLParser.LPAREN, 0)
        def condition(self):
            return self.getTypedRuleContext(RPLParser.ConditionContext,0)

        def RPAREN(self):
            return self.getToken(RPLParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenCondition" ):
                listener.enterParenCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenCondition" ):
                listener.exitParenCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenCondition" ):
                return visitor.visitParenCondition(self)
            else:
                return visitor.visitChildren(self)



    def ifClause(self):

        localctx = RPLParser.IfClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_ifClause)
        try:
            localctx = RPLParser.ParenConditionContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 142
            self.match(RPLParser.IF)
            self.state = 143
            self.match(RPLParser.LPAREN)
            self.state = 144
            self.condition(0)
            self.state = 145
            self.match(RPLParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return RPLParser.RULE_condition

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class OrConditionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RPLParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RPLParser.ConditionContext)
            else:
                return self.getTypedRuleContext(RPLParser.ConditionContext,i)

        def OR(self):
            return self.getToken(RPLParser.OR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrCondition" ):
                listener.enterOrCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrCondition" ):
                listener.exitOrCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrCondition" ):
                return visitor.visitOrCondition(self)
            else:
                return visitor.visitChildren(self)


    class AndConditionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RPLParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RPLParser.ConditionContext)
            else:
                return self.getTypedRuleContext(RPLParser.ConditionContext,i)

        def AND(self):
            return self.getToken(RPLParser.AND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndCondition" ):
                listener.enterAndCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndCondition" ):
                listener.exitAndCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndCondition" ):
                return visitor.visitAndCondition(self)
            else:
                return visitor.visitChildren(self)


    class NotConditionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RPLParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NOT(self):
            return self.getToken(RPLParser.NOT, 0)
        def condition(self):
            return self.getTypedRuleContext(RPLParser.ConditionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNotCondition" ):
                listener.enterNotCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNotCondition" ):
                listener.exitNotCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNotCondition" ):
                return visitor.visitNotCondition(self)
            else:
                return visitor.visitChildren(self)


    class ComparisonConditionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RPLParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def comparison(self):
            return self.getTypedRuleContext(RPLParser.ComparisonContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonCondition" ):
                listener.enterComparisonCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonCondition" ):
                listener.exitComparisonCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonCondition" ):
                return visitor.visitComparisonCondition(self)
            else:
                return visitor.visitChildren(self)



    def condition(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = RPLParser.ConditionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 34
        self.enterRecursionRule(localctx, 34, self.RULE_condition, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20]:
                localctx = RPLParser.NotConditionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 148
                self.match(RPLParser.NOT)
                self.state = 149
                self.condition(2)
                pass
            elif token in [32, 41, 42, 45]:
                localctx = RPLParser.ComparisonConditionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 150
                self.comparison()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 161
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 159
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
                    if la_ == 1:
                        localctx = RPLParser.AndConditionContext(self, RPLParser.ConditionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_condition)
                        self.state = 153
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 154
                        self.match(RPLParser.AND)
                        self.state = 155
                        self.condition(5)
                        pass

                    elif la_ == 2:
                        localctx = RPLParser.OrConditionContext(self, RPLParser.ConditionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_condition)
                        self.state = 156
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 157
                        self.match(RPLParser.OR)
                        self.state = 158
                        self.condition(4)
                        pass

             
                self.state = 163
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ComparisonContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RPLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(RPLParser.ExpressionContext,i)


        def comparisonOp(self):
            return self.getTypedRuleContext(RPLParser.ComparisonOpContext,0)


        def getRuleIndex(self):
            return RPLParser.RULE_comparison

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparison" ):
                listener.enterComparison(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparison" ):
                listener.exitComparison(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparison" ):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)




    def comparison(self):

        localctx = RPLParser.ComparisonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_comparison)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 164
            self.expression(0)
            self.state = 165
            self.comparisonOp()
            self.state = 166
            self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparisonOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(RPLParser.EQ, 0)

        def NE(self):
            return self.getToken(RPLParser.NE, 0)

        def LT(self):
            return self.getToken(RPLParser.LT, 0)

        def GT(self):
            return self.getToken(RPLParser.GT, 0)

        def LE(self):
            return self.getToken(RPLParser.LE, 0)

        def GE(self):
            return self.getToken(RPLParser.GE, 0)

        def getRuleIndex(self):
            return RPLParser.RULE_comparisonOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonOp" ):
                listener.enterComparisonOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonOp" ):
                listener.exitComparisonOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonOp" ):
                return visitor.visitComparisonOp(self)
            else:
                return visitor.visitChildren(self)




    def comparisonOp(self):

        localctx = RPLParser.ComparisonOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_comparisonOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 168
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 264241152) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return RPLParser.RULE_expression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class MultiDivContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RPLParser.ExpressionContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RPLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(RPLParser.ExpressionContext,i)

        def STAR(self):
            return self.getToken(RPLParser.STAR, 0)
        def DIV(self):
            return self.getToken(RPLParser.DIV, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiDiv" ):
                listener.enterMultiDiv(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiDiv" ):
                listener.exitMultiDiv(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiDiv" ):
                return visitor.visitMultiDiv(self)
            else:
                return visitor.visitChildren(self)


    class IdentifierContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RPLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENTIFIER(self):
            return self.getToken(RPLParser.IDENTIFIER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifier" ):
                listener.enterIdentifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifier" ):
                listener.exitIdentifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentifier" ):
                return visitor.visitIdentifier(self)
            else:
                return visitor.visitChildren(self)


    class MemberExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RPLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def memberAccess(self):
            return self.getTypedRuleContext(RPLParser.MemberAccessContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMemberExpr" ):
                listener.enterMemberExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMemberExpr" ):
                listener.exitMemberExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMemberExpr" ):
                return visitor.visitMemberExpr(self)
            else:
                return visitor.visitChildren(self)


    class AddSubContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RPLParser.ExpressionContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RPLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(RPLParser.ExpressionContext,i)

        def PLUS(self):
            return self.getToken(RPLParser.PLUS, 0)
        def MINUS(self):
            return self.getToken(RPLParser.MINUS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddSub" ):
                listener.enterAddSub(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddSub" ):
                listener.exitAddSub(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddSub" ):
                return visitor.visitAddSub(self)
            else:
                return visitor.visitChildren(self)


    class IntegerContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RPLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INTEGER(self):
            return self.getToken(RPLParser.INTEGER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInteger" ):
                listener.enterInteger(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInteger" ):
                listener.exitInteger(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInteger" ):
                return visitor.visitInteger(self)
            else:
                return visitor.visitChildren(self)


    class FloatContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RPLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def REAL(self):
            return self.getToken(RPLParser.REAL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFloat" ):
                listener.enterFloat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFloat" ):
                listener.exitFloat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFloat" ):
                return visitor.visitFloat(self)
            else:
                return visitor.visitChildren(self)


    class ParenExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RPLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(RPLParser.LPAREN, 0)
        def expression(self):
            return self.getTypedRuleContext(RPLParser.ExpressionContext,0)

        def RPAREN(self):
            return self.getToken(RPLParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpr" ):
                listener.enterParenExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpr" ):
                listener.exitParenExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = RPLParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 40
        self.enterRecursionRule(localctx, 40, self.RULE_expression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 179
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                localctx = RPLParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 171
                self.match(RPLParser.LPAREN)
                self.state = 172
                self.expression(0)
                self.state = 173
                self.match(RPLParser.RPAREN)
                pass

            elif la_ == 2:
                localctx = RPLParser.IntegerContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 175
                self.match(RPLParser.INTEGER)
                pass

            elif la_ == 3:
                localctx = RPLParser.FloatContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 176
                self.match(RPLParser.REAL)
                pass

            elif la_ == 4:
                localctx = RPLParser.IdentifierContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 177
                self.match(RPLParser.IDENTIFIER)
                pass

            elif la_ == 5:
                localctx = RPLParser.MemberExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 178
                self.memberAccess()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 189
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,13,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 187
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
                    if la_ == 1:
                        localctx = RPLParser.MultiDivContext(self, RPLParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 181
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 182
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==30 or _la==31):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 183
                        self.expression(8)
                        pass

                    elif la_ == 2:
                        localctx = RPLParser.AddSubContext(self, RPLParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 184
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 185
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==28 or _la==29):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 186
                        self.expression(7)
                        pass

             
                self.state = 191
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,13,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class MemberAccessContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self, i:int=None):
            if i is None:
                return self.getTokens(RPLParser.IDENTIFIER)
            else:
                return self.getToken(RPLParser.IDENTIFIER, i)

        def DOT(self):
            return self.getToken(RPLParser.DOT, 0)

        def ROLE(self):
            return self.getToken(RPLParser.ROLE, 0)

        def getRuleIndex(self):
            return RPLParser.RULE_memberAccess

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMemberAccess" ):
                listener.enterMemberAccess(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMemberAccess" ):
                listener.exitMemberAccess(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMemberAccess" ):
                return visitor.visitMemberAccess(self)
            else:
                return visitor.visitChildren(self)




    def memberAccess(self):

        localctx = RPLParser.MemberAccessContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_memberAccess)
        try:
            self.state = 198
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 192
                self.match(RPLParser.IDENTIFIER)
                self.state = 193
                self.match(RPLParser.DOT)
                self.state = 194
                self.match(RPLParser.ROLE)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 195
                self.match(RPLParser.IDENTIFIER)
                self.state = 196
                self.match(RPLParser.DOT)
                self.state = 197
                self.match(RPLParser.IDENTIFIER)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(RPLParser.STRING, 0)

        def CHARACTER(self):
            return self.getToken(RPLParser.CHARACTER, 0)

        def INTEGER(self):
            return self.getToken(RPLParser.INTEGER, 0)

        def REAL(self):
            return self.getToken(RPLParser.REAL, 0)

        def IDENTIFIER(self):
            return self.getToken(RPLParser.IDENTIFIER, 0)

        def BOOLEAN(self):
            return self.getToken(RPLParser.BOOLEAN, 0)

        def getRuleIndex(self):
            return RPLParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = RPLParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_value)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 69269232549888) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[17] = self.condition_sempred
        self._predicates[20] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def condition_sempred(self, localctx:ConditionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 6)
         




