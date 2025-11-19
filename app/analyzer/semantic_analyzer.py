from parsing.RPLParser import RPLParser
from typing import List, Dict, Any, Set
from parsing.RPLParserVisitor import RPLParserVisitor
from rich import  print
# models
from app.models.role import Role
from app.models.user import User
from app.models.group import Group
from app.models.resourse import Resource
from app.models.permission import PermissionBlock


class SemanticAnalyzer(RPLParserVisitor):
    """
    Enhanced semantic analyzer with support for:
    - Role inheritance
    - User temporal validity
    - Resource hierarchies
    - Groups
    - Policy validation
    """

    def __init__(self):
        # Symbol tables
        self.roles: Dict[str, Role] = {}
        self.users: Dict[str, User] = {}
        self.resources: Dict[str, Resource] = {}
        self.groups: Dict[str, Group] = {}

        # Error tracking
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def visitProgram(self, ctx: RPLParser.ProgramContext):
        """Visit all statements in the program."""
        print("=== Starting Semantic Analysis ===\n")

        # First pass: collect all declarations
        for statement in ctx.statement():
            self.visit(statement)

        # Validation passes
        self.validate_role_inheritance()
        self.validate_user_roles()
        self.validate_group_members()
        self.detect_circular_inheritance()

        # Report results
        self.print_results()
        print(self.get_analysis_report())

        return len(self.errors) == 0

    def visitRoleDeclaration(self, ctx: RPLParser.RoleDeclarationContext):
        """Process role declaration with optional inheritance."""
        role_name = ctx.IDENTIFIER(0).getText()
        line_number = ctx.start.line

        # Check for duplicate role
        if role_name in self.roles:
            self.add_error(ctx, f"Role '{role_name}' already declared at line {self.roles[role_name].line_number}")
            return None

        # Check for inheritance
        parent_role = None
        if ctx.EXTENDS():
            parent_role = ctx.IDENTIFIER(1).getText()

        # Extract permissions from roleBody
        permissions = []
        if ctx.roleBody():
            for role_perms_ctx in ctx.roleBody().rolePermissions():
                perms = self.visit(role_perms_ctx)
                if perms:
                    permissions.extend(perms)

        role = Role(
            name=role_name,
            permissions=permissions,
            parent_role=parent_role,
            attributes={},
            line_number=line_number
        )

        self.roles[role_name] = role
        print(f"  ✓ {role}")
        return None

    def visitRolePermissions(self, ctx: RPLParser.RolePermissionsContext):
        """Extract role permissions (both new and legacy format)."""
        permissions = []

        # New format: permissions: [{actions: [...], resources: [...]}]
        if ctx.PERMISSIONS():
            for perm_block_ctx in ctx.permissionBlock():
                perm_block = self.visit(perm_block_ctx)
                if perm_block:
                    permissions.append(perm_block)

        # Legacy format: can: [read, write] resources: [...]
        elif ctx.CAN():
            actions = []
            for perm_ctx in ctx.permission():
                actions.append(perm_ctx.getText().lower())

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

        # Build identifier path (e.g., api.users.* or database.orders)
        parts = []
        for identifier in ctx.IDENTIFIER():
            parts.append(identifier.getText())

        # Handle wildcard
        if ctx.STAR():
            parts.append('*')

        return '.'.join(parts)

    def visitUserDeclaration(self, ctx: RPLParser.UserDeclarationContext):
        """Process user declaration."""
        user_name = ctx.IDENTIFIER().getText()
        line_number = ctx.start.line

        if user_name in self.users:
            self.add_error(ctx, f"User '{user_name}' already declared at line {self.users[user_name].line_number}")
            return None

        # Extract user data
        roles = []
        valid_from = None
        valid_until = None

        if ctx.userBody():
            user_body = ctx.userBody()

            # Extract roles
            if user_body.userRoles():
                roles = self.visit(user_body.userRoles())

            # Extract validity period
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
        print(f"  ✓ {user}")
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
        """Process resource declaration."""
        resource_name = ctx.IDENTIFIER().getText()
        line_number = ctx.start.line

        if resource_name in self.resources:
            self.add_error(ctx,
                           f"Resource '{resource_name}' already declared at line {self.resources[resource_name].line_number}")
            return None

        # Extract attributes
        attributes = {}
        if ctx.resourceBody() and ctx.resourceBody().resourceAttributes():
            attributes = self.visit(ctx.resourceBody().resourceAttributes())

        resource = Resource(
            name=resource_name,
            attributes=attributes,
            children=[],
            parent=None,
            line_number=line_number
        )

        self.resources[resource_name] = resource
        print(f"  ✓ {resource}")
        return resource

    def visitResourceAttributes(self, ctx: RPLParser.ResourceAttributesContext):
        """Extract resource attributes as key-value pairs."""
        attributes = {}
        for attr_ctx in ctx.resourceAttribute():
            key = attr_ctx.IDENTIFIER().getText()
            value = self.visit(attr_ctx.value())
            attributes[key] = value
        return attributes

    def visitGroupDeclaration(self, ctx: RPLParser.GroupDeclarationContext):
        """Process group declaration."""
        group_name = ctx.IDENTIFIER().getText()
        line_number = ctx.start.line

        if group_name in self.groups:
            self.add_error(ctx, f"Group '{group_name}' already declared at line {self.groups[group_name].line_number}")
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
        print(f"  ✓ {group}")
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

    # ============================================
    # VALIDATION METHODS
    # ============================================

    def validate_role_inheritance(self):
        """Validate role inheritance references."""
        print("\n=== Validating Role Inheritance ===")
        for role_name, role in self.roles.items():
            if role.parent_role:
                if role.parent_role not in self.roles:
                    self.add_error(None,
                                   f"Role '{role_name}' (line {role.line_number}) extends undefined role '{role.parent_role}'")

    def validate_user_roles(self):
        """Validate that users reference existing roles."""
        print("\n=== Validating User Roles ===")
        for user_name, user in self.users.items():
            for role_name in user.roles:
                if role_name not in self.roles:
                    self.add_error(None,
                                   f"User '{user_name}' (line {user.line_number}) references undefined role '{role_name}'")

    def validate_group_members(self):
        """Validate that group members exist and roles are defined."""
        print("\n=== Validating Groups ===")
        for group_name, group in self.groups.items():
            # Check members
            for member in group.members:
                if member not in self.users:
                    self.add_warning(None,
                                     f"Group '{group_name}' (line {group.line_number}) references undefined user '{member}'")

            # Check roles
            for role_name in group.roles:
                if role_name not in self.roles:
                    self.add_error(None,
                                   f"Group '{group_name}' (line {group.line_number}) references undefined role '{role_name}'")

    def detect_circular_inheritance(self):
        """Detect circular role inheritance."""
        print("\n=== Checking for Circular Inheritance ===")

        def has_cycle(role_name: str, visited: Set[str], path: List[str]) -> bool:
            if role_name in visited:
                cycle_path = " -> ".join(path + [role_name])
                self.add_error(None, f"Circular inheritance detected: {cycle_path}")
                return True

            if role_name not in self.roles:
                return False

            role = self.roles[role_name]
            if not role.parent_role:
                return False

            visited.add(role_name)
            path.append(role_name)
            result = has_cycle(role.parent_role, visited, path)
            path.pop()
            visited.remove(role_name)

            return result

        for role_name in self.roles.keys():
            has_cycle(role_name, set(), [])

    # ============================================
    # ERROR HANDLING
    # ============================================

    def add_error(self, ctx, message: str):
        """Add a semantic error."""
        line = ctx.start.line if ctx else 0
        self.errors.append(f"Line {line}: ERROR: {message}")

    def add_warning(self, ctx, message: str):
        """Add a semantic warning."""
        line = ctx.start.line if ctx else 0
        self.warnings.append(f"Line {line}: WARNING: {message}")

    def print_results(self):
        """Print comprehensive analysis results."""
        print("\n" + "=" * 60)
        print("SEMANTIC ANALYSIS RESULTS")
        print("=" * 60)

        # Summary statistics
        print(f"\n📊 Symbol Table Summary:")
        print(f"   Roles:       {len(self.roles)}")
        print(f"   Users:       {len(self.users)}")
        print(f"   Resources:   {len(self.resources)}")
        print(f"   Groups:      {len(self.groups)}")

        # Detailed breakdown
        if self.roles:
            print(f"\n📋 Roles:")
            for role in self.roles.values():
                inheritance = f" extends {role.parent_role}" if role.parent_role else ""
                print(f"   - {role.name}{inheritance} ({len(role.permissions)} permission blocks)")

        if self.users:
            print(f"\n👤 Users:")
            for user in self.users.values():
                roles_str = ", ".join(user.roles)
                validity = ""
                if user.valid_from and user.valid_until:
                    validity = f" (valid: {user.valid_from} to {user.valid_until})"
                print(f"   - {user.name}: roles=[{roles_str}]{validity}")

        if self.resources:
            print(f"\n📦 Resources:")
            for resource in self.resources.values():
                attrs = ", ".join([f"{k}={v}" for k, v in resource.attributes.items()])
                print(f"   - {resource.name}: {attrs}")

        if self.groups:
            print(f"\n👥 Groups:")
            for group in self.groups.values():
                print(f"   - {group.name}: {len(group.members)} members, roles={group.roles}")

        # Errors and warnings
        print(f"\n" + "=" * 60)
        if self.errors:
            print(f"❌ {len(self.errors)} ERROR(S) FOUND:")
            for error in self.errors:
                print(f"   {error}")

        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} WARNING(S):")
            for warning in self.warnings:
                print(f"   {warning}")

        if not self.errors and not self.warnings:
            print("✅ No errors or warnings found!")
            print("   Your policy language is semantically valid.")

        print("=" * 60 + "\n")

    def get_analysis_report(self) -> Dict[str, Any]:
        """Return analysis results as a structured dictionary."""
        return {
            'success': len(self.errors) == 0,
            'statistics': {
                'roles': len(self.roles),
                'users': len(self.users),
                'resources': len(self.resources),
                'groups': len(self.groups)
            },
            'errors': self.errors,
            'warnings': self.warnings,
            'symbol_tables': {
                'roles': {name: str(role) for name, role in self.roles.items()},
                'users': {name: str(user) for name, user in self.users.items()},
                'resources': {name: str(res) for name, res in self.resources.items()},
                'groups': {name: str(group) for name, group in self.groups.items()}
            }
        }

    def get_user_permissions(self, user_name: str) -> List[PermissionBlock]:
        """Get all permissions for a user (including inherited from roles)."""
        if user_name not in self.users:
            return []

        user = self.users[user_name]
        return user.get_all_permissions(self.roles)

    def get_role_hierarchy(self, role_name: str) -> List[str]:
        """Get the complete inheritance hierarchy for a role."""
        if role_name not in self.roles:
            return []

        hierarchy = [role_name]
        current = self.roles[role_name]

        while current.parent_role:
            if current.parent_role in hierarchy:
                # Circular reference (should be caught in validation)
                break
            hierarchy.append(current.parent_role)
            if current.parent_role not in self.roles:
                break
            current = self.roles[current.parent_role]

        return hierarchy