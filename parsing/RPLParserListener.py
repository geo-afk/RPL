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


    # Enter a parse tree produced by RPLParser#rolePermissions.
    def enterRolePermissions(self, ctx:RPLParser.RolePermissionsContext):
        pass

    # Exit a parse tree produced by RPLParser#rolePermissions.
    def exitRolePermissions(self, ctx:RPLParser.RolePermissionsContext):
        pass


    # Enter a parse tree produced by RPLParser#userDeclaration.
    def enterUserDeclaration(self, ctx:RPLParser.UserDeclarationContext):
        pass

    # Exit a parse tree produced by RPLParser#userDeclaration.
    def exitUserDeclaration(self, ctx:RPLParser.UserDeclarationContext):
        pass


    # Enter a parse tree produced by RPLParser#userAttributes.
    def enterUserAttributes(self, ctx:RPLParser.UserAttributesContext):
        pass

    # Exit a parse tree produced by RPLParser#userAttributes.
    def exitUserAttributes(self, ctx:RPLParser.UserAttributesContext):
        pass


    # Enter a parse tree produced by RPLParser#userAttribute.
    def enterUserAttribute(self, ctx:RPLParser.UserAttributeContext):
        pass

    # Exit a parse tree produced by RPLParser#userAttribute.
    def exitUserAttribute(self, ctx:RPLParser.UserAttributeContext):
        pass


    # Enter a parse tree produced by RPLParser#userAssignment.
    def enterUserAssignment(self, ctx:RPLParser.UserAssignmentContext):
        pass

    # Exit a parse tree produced by RPLParser#userAssignment.
    def exitUserAssignment(self, ctx:RPLParser.UserAssignmentContext):
        pass


    # Enter a parse tree produced by RPLParser#resourceDeclaration.
    def enterResourceDeclaration(self, ctx:RPLParser.ResourceDeclarationContext):
        pass

    # Exit a parse tree produced by RPLParser#resourceDeclaration.
    def exitResourceDeclaration(self, ctx:RPLParser.ResourceDeclarationContext):
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


    # Enter a parse tree produced by RPLParser#policyRule.
    def enterPolicyRule(self, ctx:RPLParser.PolicyRuleContext):
        pass

    # Exit a parse tree produced by RPLParser#policyRule.
    def exitPolicyRule(self, ctx:RPLParser.PolicyRuleContext):
        pass


    # Enter a parse tree produced by RPLParser#policyType.
    def enterPolicyType(self, ctx:RPLParser.PolicyTypeContext):
        pass

    # Exit a parse tree produced by RPLParser#policyType.
    def exitPolicyType(self, ctx:RPLParser.PolicyTypeContext):
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


    # Enter a parse tree produced by RPLParser#resourceRef.
    def enterResourceRef(self, ctx:RPLParser.ResourceRefContext):
        pass

    # Exit a parse tree produced by RPLParser#resourceRef.
    def exitResourceRef(self, ctx:RPLParser.ResourceRefContext):
        pass


    # Enter a parse tree produced by RPLParser#parenCondition.
    def enterParenCondition(self, ctx:RPLParser.ParenConditionContext):
        pass

    # Exit a parse tree produced by RPLParser#parenCondition.
    def exitParenCondition(self, ctx:RPLParser.ParenConditionContext):
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


    # Enter a parse tree produced by RPLParser#comparisonCondition.
    def enterComparisonCondition(self, ctx:RPLParser.ComparisonConditionContext):
        pass

    # Exit a parse tree produced by RPLParser#comparisonCondition.
    def exitComparisonCondition(self, ctx:RPLParser.ComparisonConditionContext):
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


    # Enter a parse tree produced by RPLParser#multiDiv.
    def enterMultiDiv(self, ctx:RPLParser.MultiDivContext):
        pass

    # Exit a parse tree produced by RPLParser#multiDiv.
    def exitMultiDiv(self, ctx:RPLParser.MultiDivContext):
        pass


    # Enter a parse tree produced by RPLParser#identifier.
    def enterIdentifier(self, ctx:RPLParser.IdentifierContext):
        pass

    # Exit a parse tree produced by RPLParser#identifier.
    def exitIdentifier(self, ctx:RPLParser.IdentifierContext):
        pass


    # Enter a parse tree produced by RPLParser#memberExpr.
    def enterMemberExpr(self, ctx:RPLParser.MemberExprContext):
        pass

    # Exit a parse tree produced by RPLParser#memberExpr.
    def exitMemberExpr(self, ctx:RPLParser.MemberExprContext):
        pass


    # Enter a parse tree produced by RPLParser#addSub.
    def enterAddSub(self, ctx:RPLParser.AddSubContext):
        pass

    # Exit a parse tree produced by RPLParser#addSub.
    def exitAddSub(self, ctx:RPLParser.AddSubContext):
        pass


    # Enter a parse tree produced by RPLParser#integer.
    def enterInteger(self, ctx:RPLParser.IntegerContext):
        pass

    # Exit a parse tree produced by RPLParser#integer.
    def exitInteger(self, ctx:RPLParser.IntegerContext):
        pass


    # Enter a parse tree produced by RPLParser#float.
    def enterFloat(self, ctx:RPLParser.FloatContext):
        pass

    # Exit a parse tree produced by RPLParser#float.
    def exitFloat(self, ctx:RPLParser.FloatContext):
        pass


    # Enter a parse tree produced by RPLParser#parenExpr.
    def enterParenExpr(self, ctx:RPLParser.ParenExprContext):
        pass

    # Exit a parse tree produced by RPLParser#parenExpr.
    def exitParenExpr(self, ctx:RPLParser.ParenExprContext):
        pass


    # Enter a parse tree produced by RPLParser#memberAccess.
    def enterMemberAccess(self, ctx:RPLParser.MemberAccessContext):
        pass

    # Exit a parse tree produced by RPLParser#memberAccess.
    def exitMemberAccess(self, ctx:RPLParser.MemberAccessContext):
        pass


    # Enter a parse tree produced by RPLParser#value.
    def enterValue(self, ctx:RPLParser.ValueContext):
        pass

    # Exit a parse tree produced by RPLParser#value.
    def exitValue(self, ctx:RPLParser.ValueContext):
        pass



del RPLParser