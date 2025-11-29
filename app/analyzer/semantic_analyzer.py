from datetime import datetime

from app.api.services.roles_service import RoleService
from app.api.validation.semantic_validation import SemanticValidation
from parsing.RPLParserVisitor import RPLParserVisitor
from parsing.RPLParser import RPLParser
from typing import Dict, List, Optional, Sequence
# models
from app.models.role import Role
from app.models.user import User
from app.models.group import Group
from app.models.resource import Resource, ResourceType
from app.models.permission import PermissionBlock


class SemanticAnalyzer(RPLParserVisitor):

    def __init__(self):
        # Symbol tables
        self.roles: Dict[str, Role] = {}
        self.users: Dict[str, User] = {}
        self.resources: Dict[str, Resource] = {}
        self.groups: Dict[str, Group] = {}

        self.validator = SemanticValidation()

    def visitProgram(self, ctx: RPLParser.ProgramContext):
        """Visit all statements in the program."""

        # First pass: collect all declarations
        for statement in ctx.statement():
            self.visit(statement)

        self.validator.get_values(self.roles, self.users, self.resources, self.groups)
        self.validator.run_all()

        return len(self.validator.errors) == 0

    def visitRoleDeclaration(self, ctx: RPLParser.RoleDeclarationContext) -> None:
        """Process role declaration with optional inheritance."""
        role_name = ctx.IDENTIFIER(0).getText()
        line_number = ctx.start.line

        role_service = RoleService()
        db_roles: Sequence[Role] = role_service.get_roles()
        for r in db_roles:
            self.roles[r.name] = r

        if role_name in self.roles:
            self.validator.add_error(ctx,
                                     f"Role '{role_name}' already declared at line {self.roles[role_name].line_number}")
            return None

        parent: Role | None = None
        if ctx.EXTENDS():
            parent_role = ctx.IDENTIFIER(1).getText()

            if parent_role in self.roles:
                parent = self.roles[parent_role]

        permissions = []
        if ctx.roleBody():
            for role_perms_ctx in ctx.roleBody().rolePermissions():
                perms = self.visit(role_perms_ctx)
                if perms:
                    permissions.extend(perms)

        role = Role(
            name=role_name,
            permissions=permissions,
            parent_role=parent,
            attributes={},
            line_number=line_number
        )

        self.roles[role_name] = role
        return None

    def visitRolePermissions(self, ctx: RPLParser.RolePermissionsContext):
        """Extract role permissions (both new and legacy format)."""
        permissions = []

        # New format: permissions: [{actions: [...], resources: [...]}]
        if ctx.PERMISSIONS():
            for perm_block_ctx in ctx.permissionBlock():
                perm_block: PermissionBlock = self.visit(perm_block_ctx)
                if perm_block:
                    permissions.append(perm_block)

        # Legacy format: can: [read, write] resources: [...]
        elif ctx.CAN():
            actions = []
            for perm_ctx in ctx.permission():
                if perm_ctx.getText() != '*':
                    actions.append(perm_ctx.getText().lower())
                if perm_ctx.getText() == '*':
                    actions.append(perm_ctx.getText())


            resources = []
            if ctx.resourceList():
                resources = self.visit(ctx.resourceList())

            permissions.append(PermissionBlock(actions=actions, resources=resources))

        return permissions

    def visitPermissionBlock(self, ctx: RPLParser.PermissionBlockContext):
        """Extract a permission block."""
        actions = []
        resources = []
        conditions = None

        # Extract actions
        if ctx.actionList():
            actions = self.visit(ctx.actionList())

        # Extract resources
        if ctx.resourceList():
            resources = self.visit(ctx.resourceList())

        # Extract conditions if present
        if ctx.condition():
            conditions = ctx.condition().getText()

        return PermissionBlock(actions=actions, resources=resources, conditions=conditions)

    def visitActionList(self, ctx: RPLParser.ActionListContext):
        """Extract list of actions."""
        actions = []
        for perm_ctx in ctx.permission():
            if perm_ctx.getText() == '*':
                actions.append(perm_ctx.getText())
            else:
                actions.append(perm_ctx.getText().lower())
        return actions

    def visitResourceList(self, ctx: RPLParser.ResourceListContext):
        """Extract list of resource references."""
        resources = []
        for res_ctx in ctx.resourceRef():
            resources.append(self.visit(res_ctx))
        return resources

    def visitResourceRef(self, ctx: RPLParser.ResourceRefContext):
        """Extract resource reference (identifier path or string)."""
        if ctx.STRING():
            return ctx.STRING().getText().strip('"\'')

        # Build identifier path (e.g., api.users.* or client_db.orders)
        parts = []
        for identifier in ctx.IDENTIFIER():
            parts.append(identifier.getText())

        # Handle wildcard
        if ctx.STAR():
            parts.append('*')

        return '.'.join(parts)

    def visitUserDeclaration(self, ctx: RPLParser.UserDeclarationContext) -> None:
        """Process user declaration."""
        user_name: str = ctx.IDENTIFIER().getText()
        line_number: int = ctx.start.line

        if user_name in self.users:
            self.validator.add_error(
                ctx,
                f"User '{user_name}' already declared at line {self.users[user_name].line_number}"
            )
            return None

        # Extract user data
        roles: List[Role] = []
        valid_from: Optional[datetime] = None
        valid_until: Optional[datetime] = None

        if ctx.userBody():
            user_body = ctx.userBody()

            # Extract roles
            if user_body.userRoles():
                role_names: List[str] = self.visit(user_body.userRoles())

                role_service = RoleService()
                db_roles: Sequence[Role] = role_service.get_roles()
                for r in db_roles:
                    self.roles[r.name] = r

                for role_name in role_names:
                    if role_name not in self.roles:
                        self.validator.add_error(ctx, f"Role '{role_name}' not declared")
                    else:
                        roles.append(self.roles[role_name])

            if user_body.validPeriod():
                valid_from, valid_until = self.visit(user_body.validPeriod())

        user = User(
            name=user_name,
            roles=roles,
            attributes={},
            valid_from=valid_from,
            valid_until=valid_until,
            line_number=line_number
        )

        self.users[user_name] = user
        return None

    def visitUserRoles(self, ctx: RPLParser.UserRolesContext):
        """Extract user roles."""
        roles = []
        for identifier in ctx.IDENTIFIER():
            roles.append(identifier.getText())
        return roles

    def visitValidPeriod(self, ctx: RPLParser.ValidPeriodContext):
        """Extract validity period (valid_from, valid_until)."""
        valid_from = self.visit(ctx.validFrom())
        valid_until = self.visit(ctx.validUntil())
        return valid_from, valid_until

    def visitValidFrom(self, ctx: RPLParser.ValidFromContext):
        """Extract valid_from date."""
        return ctx.STRING().getText().strip('"\'')

    def visitValidUntil(self, ctx: RPLParser.ValidUntilContext):
        """Extract valid_until date."""
        return ctx.STRING().getText().strip('"\'')

    def visitResourceDeclaration(self, ctx: RPLParser.ResourceDeclarationContext):
        """Process resource declaration with path, type, and metadata."""
        resource_name = ctx.IDENTIFIER().getText()
        line_number = ctx.start.line

        if resource_name in self.resources:
            self.validator.add_error(
                ctx,
                f"Resource '{resource_name}' already declared at line {self.resources[resource_name].line_number}"
            )
            return None

        path: Optional[str] = None
        resource_type: Optional[ResourceType] = None
        metadata: Dict[str, any] = {}

        if ctx.resourceBody():
            for prop_ctx in ctx.resourceBody().resourceProperty():
                if prop_ctx.PATH():
                    # Now correctly access the STRING token directly
                    string_token = prop_ctx.STRING()
                    if string_token:
                        path = string_token.getText().strip('"\'')
                    else:
                        self.validator.add_error(ctx, f"PATH property missing value for resource '{resource_name}'")

                elif prop_ctx.TYPE():
                    type_ctx = prop_ctx.resourceType()
                    type_text = type_ctx.getText().lower()

                    try:
                        resource_type = ResourceType(type_text)
                    except ValueError:
                        valid_types = ', '.join([e.value for e in ResourceType])
                        self.validator.add_error(
                            ctx,
                            f"Invalid resource type '{type_text}'. Must be one of: {valid_types}"
                        )

                elif prop_ctx.METADATA():
                    meta_block_ctx = prop_ctx.metadataBlock()
                    if meta_block_ctx:
                        metadata = self.visit(meta_block_ctx)

        # Validate required fields
        if path is None:
            self.validator.add_error(ctx, f"Resource '{resource_name}' missing required 'path' property")
            return None

        if resource_type is None:
            self.validator.add_error(ctx, f"Resource '{resource_name}' missing required 'type' property")
            return None

        resource = Resource(
            name=resource_name,
            path=path,
            resource_type=resource_type,
            meta=metadata,
            line_number=line_number
        )

        self.resources[resource_name] = resource
        return resource

    def visitMetadataBlock(self, ctx: RPLParser.MetadataBlockContext):
        """Extract metadata block as key-value pairs."""
        metadata = {}

        if ctx.metadataEntry():
            for entry_ctx in ctx.metadataEntry():
                key = entry_ctx.IDENTIFIER().getText()
                value = self.visit(entry_ctx.value())
                metadata[key] = value

        return metadata

    def visitGroupDeclaration(self, ctx: RPLParser.GroupDeclarationContext):
        """Process group declaration."""
        group_name = ctx.IDENTIFIER().getText()
        line_number = ctx.start.line

        if group_name in self.groups:
            self.validator.add_error(ctx,
                                     f"Group '{group_name}' already declared at line {self.groups[group_name].line_number}")
            return None

        members = []
        roles = []

        if ctx.groupBody():
            group_body = ctx.groupBody()

            if group_body.groupMembers():
                members = self.visit(group_body.groupMembers())

            if group_body.groupRoles():
                roles = self.visit(group_body.groupRoles())

        group = Group(
            name=group_name,
            members=members,
            roles=roles,
            line_number=line_number
        )

        self.groups[group_name] = group
        return None

    def visitGroupMembers(self, ctx: RPLParser.GroupMembersContext):
        """Extract group members."""
        return self.visit(ctx.memberList())

    def visitMemberList(self, ctx: RPLParser.MemberListContext):
        """Extract list of member names."""
        members = []
        for identifier in ctx.IDENTIFIER():
            members.append(identifier.getText())
        return members

    def visitGroupRoles(self, ctx: RPLParser.GroupRolesContext):
        """Extract group roles."""
        roles = []
        for identifier in ctx.IDENTIFIER():
            roles.append(identifier.getText())
        return roles

    def visitValue(self, ctx: RPLParser.ValueContext):
        """Extract value (string, number, identifier, boolean, array)."""
        if ctx.STRING():
            return ctx.STRING().getText().strip('"\'')
        elif ctx.CHARACTER():
            return ctx.CHARACTER().getText().strip("'")
        elif ctx.INTEGER():
            return int(ctx.INTEGER().getText())
        elif ctx.REAL():
            return float(ctx.REAL().getText())
        elif ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        elif ctx.BOOLEAN():
            return ctx.BOOLEAN().getText().lower() == 'true'
        elif ctx.valueList():
            return self.visit(ctx.valueList())
        return None

    def visitValueList(self, ctx: RPLParser.ValueListContext):
        """Extract list of values."""
        values = []
        for value_ctx in ctx.value():
            values.append(self.visit(value_ctx))
        return values