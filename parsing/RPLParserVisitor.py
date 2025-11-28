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


    # Visit a parse tree produced by RPLParser#roleBody.
    def visitRoleBody(self, ctx:RPLParser.RoleBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#rolePermissions.
    def visitRolePermissions(self, ctx:RPLParser.RolePermissionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#permissionBlock.
    def visitPermissionBlock(self, ctx:RPLParser.PermissionBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#userDeclaration.
    def visitUserDeclaration(self, ctx:RPLParser.UserDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#userBody.
    def visitUserBody(self, ctx:RPLParser.UserBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#validPeriod.
    def visitValidPeriod(self, ctx:RPLParser.ValidPeriodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#userRoles.
    def visitUserRoles(self, ctx:RPLParser.UserRolesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#validFrom.
    def visitValidFrom(self, ctx:RPLParser.ValidFromContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#validUntil.
    def visitValidUntil(self, ctx:RPLParser.ValidUntilContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#resourceDeclaration.
    def visitResourceDeclaration(self, ctx:RPLParser.ResourceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#resourceBody.
    def visitResourceBody(self, ctx:RPLParser.ResourceBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#resourceProperty.
    def visitResourceProperty(self, ctx:RPLParser.ResourcePropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#resourceType.
    def visitResourceType(self, ctx:RPLParser.ResourceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#metadataBlock.
    def visitMetadataBlock(self, ctx:RPLParser.MetadataBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#metadataEntry.
    def visitMetadataEntry(self, ctx:RPLParser.MetadataEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#resourceList.
    def visitResourceList(self, ctx:RPLParser.ResourceListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#resourceRef.
    def visitResourceRef(self, ctx:RPLParser.ResourceRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#groupDeclaration.
    def visitGroupDeclaration(self, ctx:RPLParser.GroupDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#groupBody.
    def visitGroupBody(self, ctx:RPLParser.GroupBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#groupMembers.
    def visitGroupMembers(self, ctx:RPLParser.GroupMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#memberList.
    def visitMemberList(self, ctx:RPLParser.MemberListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#groupRoles.
    def visitGroupRoles(self, ctx:RPLParser.GroupRolesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#actionList.
    def visitActionList(self, ctx:RPLParser.ActionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#permission.
    def visitPermission(self, ctx:RPLParser.PermissionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#condition.
    def visitCondition(self, ctx:RPLParser.ConditionContext):
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


    # Visit a parse tree produced by RPLParser#primaryCondition.
    def visitPrimaryCondition(self, ctx:RPLParser.PrimaryConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#comparison.
    def visitComparison(self, ctx:RPLParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#comparisonOp.
    def visitComparisonOp(self, ctx:RPLParser.ComparisonOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#expression.
    def visitExpression(self, ctx:RPLParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#additiveExpr.
    def visitAdditiveExpr(self, ctx:RPLParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#multiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:RPLParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#unaryExpr.
    def visitUnaryExpr(self, ctx:RPLParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#primaryExpr.
    def visitPrimaryExpr(self, ctx:RPLParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#atom.
    def visitAtom(self, ctx:RPLParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#qualifiedName.
    def visitQualifiedName(self, ctx:RPLParser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#value.
    def visitValue(self, ctx:RPLParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RPLParser#valueList.
    def visitValueList(self, ctx:RPLParser.ValueListContext):
        return self.visitChildren(ctx)



del RPLParser