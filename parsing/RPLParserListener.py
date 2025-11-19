# Generated from RPLParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .RPLParser import RPLParser
else:
    from RPLParser import RPLParser

# This class defines a complete listener for a parse tree produced by RPLParser.
class RPLParserListener(ParseTreeListener):

    # Enter a parse tree produced by RPLParser#program.
    def enterProgram(self, ctx:RPLParser.ProgramContext):
        pass

    # Exit a parse tree produced by RPLParser#program.
    def exitProgram(self, ctx:RPLParser.ProgramContext):
        pass


    # Enter a parse tree produced by RPLParser#statement.
    def enterStatement(self, ctx:RPLParser.StatementContext):
        pass

    # Exit a parse tree produced by RPLParser#statement.
    def exitStatement(self, ctx:RPLParser.StatementContext):
        pass


    # Enter a parse tree produced by RPLParser#roleDeclaration.
    def enterRoleDeclaration(self, ctx:RPLParser.RoleDeclarationContext):
        pass

    # Exit a parse tree produced by RPLParser#roleDeclaration.
    def exitRoleDeclaration(self, ctx:RPLParser.RoleDeclarationContext):
        pass


    # Enter a parse tree produced by RPLParser#roleBody.
    def enterRoleBody(self, ctx:RPLParser.RoleBodyContext):
        pass

    # Exit a parse tree produced by RPLParser#roleBody.
    def exitRoleBody(self, ctx:RPLParser.RoleBodyContext):
        pass


    # Enter a parse tree produced by RPLParser#rolePermissions.
    def enterRolePermissions(self, ctx:RPLParser.RolePermissionsContext):
        pass

    # Exit a parse tree produced by RPLParser#rolePermissions.
    def exitRolePermissions(self, ctx:RPLParser.RolePermissionsContext):
        pass


    # Enter a parse tree produced by RPLParser#permissionBlock.
    def enterPermissionBlock(self, ctx:RPLParser.PermissionBlockContext):
        pass

    # Exit a parse tree produced by RPLParser#permissionBlock.
    def exitPermissionBlock(self, ctx:RPLParser.PermissionBlockContext):
        pass


    # Enter a parse tree produced by RPLParser#userDeclaration.
    def enterUserDeclaration(self, ctx:RPLParser.UserDeclarationContext):
        pass

    # Exit a parse tree produced by RPLParser#userDeclaration.
    def exitUserDeclaration(self, ctx:RPLParser.UserDeclarationContext):
        pass


    # Enter a parse tree produced by RPLParser#userBody.
    def enterUserBody(self, ctx:RPLParser.UserBodyContext):
        pass

    # Exit a parse tree produced by RPLParser#userBody.
    def exitUserBody(self, ctx:RPLParser.UserBodyContext):
        pass


    # Enter a parse tree produced by RPLParser#validPeriod.
    def enterValidPeriod(self, ctx:RPLParser.ValidPeriodContext):
        pass

    # Exit a parse tree produced by RPLParser#validPeriod.
    def exitValidPeriod(self, ctx:RPLParser.ValidPeriodContext):
        pass


    # Enter a parse tree produced by RPLParser#userRoles.
    def enterUserRoles(self, ctx:RPLParser.UserRolesContext):
        pass

    # Exit a parse tree produced by RPLParser#userRoles.
    def exitUserRoles(self, ctx:RPLParser.UserRolesContext):
        pass


    # Enter a parse tree produced by RPLParser#validFrom.
    def enterValidFrom(self, ctx:RPLParser.ValidFromContext):
        pass

    # Exit a parse tree produced by RPLParser#validFrom.
    def exitValidFrom(self, ctx:RPLParser.ValidFromContext):
        pass


    # Enter a parse tree produced by RPLParser#validUntil.
    def enterValidUntil(self, ctx:RPLParser.ValidUntilContext):
        pass

    # Exit a parse tree produced by RPLParser#validUntil.
    def exitValidUntil(self, ctx:RPLParser.ValidUntilContext):
        pass


    # Enter a parse tree produced by RPLParser#resourceDeclaration.
    def enterResourceDeclaration(self, ctx:RPLParser.ResourceDeclarationContext):
        pass

    # Exit a parse tree produced by RPLParser#resourceDeclaration.
    def exitResourceDeclaration(self, ctx:RPLParser.ResourceDeclarationContext):
        pass


    # Enter a parse tree produced by RPLParser#resourceBody.
    def enterResourceBody(self, ctx:RPLParser.ResourceBodyContext):
        pass

    # Exit a parse tree produced by RPLParser#resourceBody.
    def exitResourceBody(self, ctx:RPLParser.ResourceBodyContext):
        pass


    # Enter a parse tree produced by RPLParser#resourceAttributes.
    def enterResourceAttributes(self, ctx:RPLParser.ResourceAttributesContext):
        pass

    # Exit a parse tree produced by RPLParser#resourceAttributes.
    def exitResourceAttributes(self, ctx:RPLParser.ResourceAttributesContext):
        pass


    # Enter a parse tree produced by RPLParser#resourceAttribute.
    def enterResourceAttribute(self, ctx:RPLParser.ResourceAttributeContext):
        pass

    # Exit a parse tree produced by RPLParser#resourceAttribute.
    def exitResourceAttribute(self, ctx:RPLParser.ResourceAttributeContext):
        pass


    # Enter a parse tree produced by RPLParser#resourceList.
    def enterResourceList(self, ctx:RPLParser.ResourceListContext):
        pass

    # Exit a parse tree produced by RPLParser#resourceList.
    def exitResourceList(self, ctx:RPLParser.ResourceListContext):
        pass


    # Enter a parse tree produced by RPLParser#resourceRef.
    def enterResourceRef(self, ctx:RPLParser.ResourceRefContext):
        pass

    # Exit a parse tree produced by RPLParser#resourceRef.
    def exitResourceRef(self, ctx:RPLParser.ResourceRefContext):
        pass


    # Enter a parse tree produced by RPLParser#groupDeclaration.
    def enterGroupDeclaration(self, ctx:RPLParser.GroupDeclarationContext):
        pass

    # Exit a parse tree produced by RPLParser#groupDeclaration.
    def exitGroupDeclaration(self, ctx:RPLParser.GroupDeclarationContext):
        pass


    # Enter a parse tree produced by RPLParser#groupBody.
    def enterGroupBody(self, ctx:RPLParser.GroupBodyContext):
        pass

    # Exit a parse tree produced by RPLParser#groupBody.
    def exitGroupBody(self, ctx:RPLParser.GroupBodyContext):
        pass


    # Enter a parse tree produced by RPLParser#groupMembers.
    def enterGroupMembers(self, ctx:RPLParser.GroupMembersContext):
        pass

    # Exit a parse tree produced by RPLParser#groupMembers.
    def exitGroupMembers(self, ctx:RPLParser.GroupMembersContext):
        pass


    # Enter a parse tree produced by RPLParser#memberList.
    def enterMemberList(self, ctx:RPLParser.MemberListContext):
        pass

    # Exit a parse tree produced by RPLParser#memberList.
    def exitMemberList(self, ctx:RPLParser.MemberListContext):
        pass


    # Enter a parse tree produced by RPLParser#groupRoles.
    def enterGroupRoles(self, ctx:RPLParser.GroupRolesContext):
        pass

    # Exit a parse tree produced by RPLParser#groupRoles.
    def exitGroupRoles(self, ctx:RPLParser.GroupRolesContext):
        pass


    # Enter a parse tree produced by RPLParser#actionList.
    def enterActionList(self, ctx:RPLParser.ActionListContext):
        pass

    # Exit a parse tree produced by RPLParser#actionList.
    def exitActionList(self, ctx:RPLParser.ActionListContext):
        pass


    # Enter a parse tree produced by RPLParser#permission.
    def enterPermission(self, ctx:RPLParser.PermissionContext):
        pass

    # Exit a parse tree produced by RPLParser#permission.
    def exitPermission(self, ctx:RPLParser.PermissionContext):
        pass


    # Enter a parse tree produced by RPLParser#condition.
    def enterCondition(self, ctx:RPLParser.ConditionContext):
        pass

    # Exit a parse tree produced by RPLParser#condition.
    def exitCondition(self, ctx:RPLParser.ConditionContext):
        pass


    # Enter a parse tree produced by RPLParser#orCondition.
    def enterOrCondition(self, ctx:RPLParser.OrConditionContext):
        pass

    # Exit a parse tree produced by RPLParser#orCondition.
    def exitOrCondition(self, ctx:RPLParser.OrConditionContext):
        pass


    # Enter a parse tree produced by RPLParser#andCondition.
    def enterAndCondition(self, ctx:RPLParser.AndConditionContext):
        pass

    # Exit a parse tree produced by RPLParser#andCondition.
    def exitAndCondition(self, ctx:RPLParser.AndConditionContext):
        pass


    # Enter a parse tree produced by RPLParser#notCondition.
    def enterNotCondition(self, ctx:RPLParser.NotConditionContext):
        pass

    # Exit a parse tree produced by RPLParser#notCondition.
    def exitNotCondition(self, ctx:RPLParser.NotConditionContext):
        pass


    # Enter a parse tree produced by RPLParser#primaryCondition.
    def enterPrimaryCondition(self, ctx:RPLParser.PrimaryConditionContext):
        pass

    # Exit a parse tree produced by RPLParser#primaryCondition.
    def exitPrimaryCondition(self, ctx:RPLParser.PrimaryConditionContext):
        pass


    # Enter a parse tree produced by RPLParser#comparison.
    def enterComparison(self, ctx:RPLParser.ComparisonContext):
        pass

    # Exit a parse tree produced by RPLParser#comparison.
    def exitComparison(self, ctx:RPLParser.ComparisonContext):
        pass


    # Enter a parse tree produced by RPLParser#comparisonOp.
    def enterComparisonOp(self, ctx:RPLParser.ComparisonOpContext):
        pass

    # Exit a parse tree produced by RPLParser#comparisonOp.
    def exitComparisonOp(self, ctx:RPLParser.ComparisonOpContext):
        pass


    # Enter a parse tree produced by RPLParser#expression.
    def enterExpression(self, ctx:RPLParser.ExpressionContext):
        pass

    # Exit a parse tree produced by RPLParser#expression.
    def exitExpression(self, ctx:RPLParser.ExpressionContext):
        pass


    # Enter a parse tree produced by RPLParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:RPLParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by RPLParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:RPLParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by RPLParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:RPLParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by RPLParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:RPLParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by RPLParser#unaryExpr.
    def enterUnaryExpr(self, ctx:RPLParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by RPLParser#unaryExpr.
    def exitUnaryExpr(self, ctx:RPLParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by RPLParser#primaryExpr.
    def enterPrimaryExpr(self, ctx:RPLParser.PrimaryExprContext):
        pass

    # Exit a parse tree produced by RPLParser#primaryExpr.
    def exitPrimaryExpr(self, ctx:RPLParser.PrimaryExprContext):
        pass


    # Enter a parse tree produced by RPLParser#atom.
    def enterAtom(self, ctx:RPLParser.AtomContext):
        pass

    # Exit a parse tree produced by RPLParser#atom.
    def exitAtom(self, ctx:RPLParser.AtomContext):
        pass


    # Enter a parse tree produced by RPLParser#qualifiedName.
    def enterQualifiedName(self, ctx:RPLParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by RPLParser#qualifiedName.
    def exitQualifiedName(self, ctx:RPLParser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by RPLParser#value.
    def enterValue(self, ctx:RPLParser.ValueContext):
        pass

    # Exit a parse tree produced by RPLParser#value.
    def exitValue(self, ctx:RPLParser.ValueContext):
        pass


    # Enter a parse tree produced by RPLParser#valueList.
    def enterValueList(self, ctx:RPLParser.ValueListContext):
        pass

    # Exit a parse tree produced by RPLParser#valueList.
    def exitValueList(self, ctx:RPLParser.ValueListContext):
        pass



del RPLParser