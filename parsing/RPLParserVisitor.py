# Generated from RPLParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .RPLParser import RPLParser
else:
    from RPLParser import RPLParser

# This class defines a complete generic visitor for a parse tree produced by RPLParser.

class RPLParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by RPLParser#program.
    def visitProgram(self, ctx:RPLParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#statement.
    def visitStatement(self, ctx:RPLParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#roleDeclaration.
    def visitRoleDeclaration(self, ctx:RPLParser.RoleDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#rolePermissions.
    def visitRolePermissions(self, ctx:RPLParser.RolePermissionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#userDeclaration.
    def visitUserDeclaration(self, ctx:RPLParser.UserDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#userAttributes.
    def visitUserAttributes(self, ctx:RPLParser.UserAttributesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#userAttribute.
    def visitUserAttribute(self, ctx:RPLParser.UserAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#userAssignment.
    def visitUserAssignment(self, ctx:RPLParser.UserAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#resourceDeclaration.
    def visitResourceDeclaration(self, ctx:RPLParser.ResourceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#resourceAttributes.
    def visitResourceAttributes(self, ctx:RPLParser.ResourceAttributesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#resourceAttribute.
    def visitResourceAttribute(self, ctx:RPLParser.ResourceAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#policyRule.
    def visitPolicyRule(self, ctx:RPLParser.PolicyRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#policyType.
    def visitPolicyType(self, ctx:RPLParser.PolicyTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#actionList.
    def visitActionList(self, ctx:RPLParser.ActionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#permission.
    def visitPermission(self, ctx:RPLParser.PermissionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#resourceRef.
    def visitResourceRef(self, ctx:RPLParser.ResourceRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#parenCondition.
    def visitParenCondition(self, ctx:RPLParser.ParenConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#orCondition.
    def visitOrCondition(self, ctx:RPLParser.OrConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#andCondition.
    def visitAndCondition(self, ctx:RPLParser.AndConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#notCondition.
    def visitNotCondition(self, ctx:RPLParser.NotConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#comparisonCondition.
    def visitComparisonCondition(self, ctx:RPLParser.ComparisonConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#comparison.
    def visitComparison(self, ctx:RPLParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#comparisonOp.
    def visitComparisonOp(self, ctx:RPLParser.ComparisonOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#multiDiv.
    def visitMultiDiv(self, ctx:RPLParser.MultiDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#identifier.
    def visitIdentifier(self, ctx:RPLParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#memberExpr.
    def visitMemberExpr(self, ctx:RPLParser.MemberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#addSub.
    def visitAddSub(self, ctx:RPLParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#integer.
    def visitInteger(self, ctx:RPLParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#float.
    def visitFloat(self, ctx:RPLParser.FloatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#parenExpr.
    def visitParenExpr(self, ctx:RPLParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#memberAccess.
    def visitMemberAccess(self, ctx:RPLParser.MemberAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#value.
    def visitValue(self, ctx:RPLParser.ValueContext):
        return self.visitChildren(ctx)



del RPLParser