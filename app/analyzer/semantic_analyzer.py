from parsing.RPLParser import RPLParser
from parsing.RPLParserVisitor import RPLParserVisitor



class SemanticAnalyzer(RPLParserVisitor):
    """
    Performs semantic analysis on the SPL parse tree.
    Checks for:
    - Undefined roles, users, resources
    - Type consistency
    - Conflicting policies
    - Scope and binding issues
    """

    def __init__(self):
        self.roles = {}  # role_name -> permissions
        self.users = {}  # user_name -> attributes
        self.resources = {}  # resource_name -> attributes
        self.policies = []  # list of policy rules
        self.errors = []  # semantic errors
        self.warnings = []  # semantic warnings

    def visitProgram(self, ctx: RPLParser.ProgramContext):
        """Visit all statements in the program."""
        print("=== Starting Semantic Analysis ===")

        # First pass: collect declarations
        for statement in ctx.statement():
            self.visit(statement)

        # Second pass: validate policies
        self.validate_policies()

        # Report results
        self.print_results()

        return self.errors == []  # Return True if no errors

    def visitRoleDeclaration(self, ctx: RPLParser.RoleDeclarationContext):
        """Process role declaration."""
        role_name = ctx.IDENTIFIER().getText()

        # Check for duplicate role
        if role_name in self.roles.keys():
            self.add_error(ctx, f"Role '{role_name}' already declared")
            return

        # Extract permissions
        permissions = self.visit(ctx.rolePermissions())
        self.roles[role_name] = permissions

        print(f"  Declared role: {role_name} with permissions: {permissions}")
        return None

    def visitRolePermissions(self, ctx: RPLParser.RolePermissionsContext):
        """Extract list of permissions."""
        permissions = []
        for perm_ctx in ctx.permission():
            perm_text = perm_ctx.getText()
            permissions.append(perm_text)
        return permissions

    def visitUserDeclaration(self, ctx: RPLParser.UserDeclarationContext):
        """Process user declaration."""
        user_name = ctx.IDENTIFIER().getText()

        # Check for duplicate user
        if user_name in self.users:
            self.add_error(ctx, f"User '{user_name}' already declared")
            return


        key: str = ctx.userAttributes().userAssignment().getText()
        value: str = ctx.userAttributes().userAttribute().getText().split(",")
        self.users[user_name] = {}

        temp_keys = self.roles.copy()
        keys = temp_keys.keys()
        for key in keys:
            key.capitalize()

        attributes = {}
        for role in value:
            attributes[key] = role

            if key == 'role' and value not in keys:
                self.add_error(ctx,
                               f"User '{user_name}' references undefined role '{value}'")

        self.users[user_name] = attributes
        print(f"  Declared user: {user_name} with attributes: {attributes}")
        return None


    def visitResourceDeclaration(self, ctx: RPLParser.ResourceDeclarationContext):
        """Process resource declaration."""
        resource_name = ctx.IDENTIFIER().getText()

        if resource_name in self.resources:
            self.add_error(ctx, f"Resource '{resource_name}' already declared")
            return

        # Extract attributes
        attributes = {}
        for attr_ctx in ctx.resourceAttributes().resourceAttribute():
            key = attr_ctx.IDENTIFIER().getText()
            value = self.visit(attr_ctx.value())
            attributes[key] = value

        self.resources[resource_name] = attributes
        print(f"  Declared resource: {resource_name}")
        return None

    def visitPolicyRule(self, ctx: RPLParser.PolicyRuleContext):
        """Process policy rule."""
        policy_type = ctx.policyType().getText()
        actions = [a.getText() for a in ctx.actionList().permission()]
        resource_ref = ctx.resourceRef().getText().strip('"\'')

        # Check if resource exists (if not a wildcard)
        if '*' not in resource_ref and resource_ref not in self.resources:
            self.add_warning(ctx,
                             f"Policy references undefined resource '{resource_ref}'")

        # Store policy for later analysis
        policy = {
            'type': policy_type,
            'actions': actions,
            'resource': resource_ref,
            'condition': self.visit(ctx.ifClause()) if ctx.ifClause() else None,
            'line': ctx.start.line
        }
        self.policies.append(policy)

        print(f"  Policy: {policy_type} {actions} ON {resource_ref}")
        return None

    def visitValue(self, ctx: RPLParser.ValueContext):
        """Extract value (string, number, identifier, boolean)."""
        if ctx.STRING():
            return ctx.STRING().getText().strip('"\'')
        elif ctx.NUMBER():
            text = ctx.NUMBER().getText()
            return float(text) if '.' in text else int(text)
        elif ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        elif ctx.BOOLEAN():
            return ctx.BOOLEAN().getText() == 'true'
        return None

    def validate_policies(self):
        """Check for conflicting or overlapping policies."""
        print("\n=== Validating Policies ===")

        # Group policies by resource
        by_resource = {}
        for policy in self.policies:
            resource = policy['resource']
            if resource not in by_resource:
                by_resource[resource] = []
            by_resource[resource].append(policy)

        # Check for conflicts
        for resource, policies in by_resource.items():
            allow_policies = [p for p in policies if p['type'] == 'ALLOW']
            deny_policies = [p for p in policies if p['type'] == 'DENY']

            # Check for contradictory policies
            for allow_pol in allow_policies:
                for deny_pol in deny_policies:
                    common_actions = set(allow_pol['actions']) & set(deny_pol['actions'])
                    if common_actions:
                        self.add_warning(None,
                                         f"Conflicting policies on resource '{resource}' "
                                         f"for actions {common_actions}. "
                                         f"DENY (line {deny_pol['line']}) overrides "
                                         f"ALLOW (line {allow_pol['line']})")

    def add_error(self, ctx, message):
        """Add a semantic error."""
        line = ctx.start.line if ctx else 0
        self.errors.append(f"Line {line}: ERROR: {message}")

    def add_warning(self, ctx, message):
        """Add a semantic warning."""
        line = ctx.start.line if ctx else 0
        self.warnings.append(f"Line {line}: WARNING: {message}")

    def print_results(self):
        """Print analysis results."""
        print("\n=== Semantic Analysis Results ===")
        print(f"Roles: {len(self.roles)}")
        print(f"Users: {len(self.users)}")
        print(f"Resources: {len(self.resources)}")
        print(f"Policies: {len(self.policies)}")

        if self.errors:
            print(f"\n❌ {len(self.errors)} ERROR(S):")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} WARNING(S):")
            for warning in self.warnings:
                print(f"  {warning}")

        if not self.errors and not self.warnings:
            print("\n✓ No errors or warnings found")