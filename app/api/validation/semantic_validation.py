from typing import Dict, List
from app.models.permission import PermissionBlock
from app.models.role import Role
from app.models.user import User
from app.models.group import Group
from app.models.resource import Resource
from app.models.error_response import WarningResponse, ErrorResponse


class SemanticValidation:

    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self.users: Dict[str, User] = {}
        self.resources: Dict[str, Resource] = {}
        self.groups: Dict[str, Group] = {}

        self.errors: List[ErrorResponse] = []
        self.warnings: List[WarningResponse] = []

    def get_values(
        self,
        roles: Dict[str, Role],
        users: Dict[str, User],
        resources: Dict[str, Resource],
        groups: Dict[str, Group]
    ):
        self.roles = roles
        self.users = users
        self.resources = resources
        self.groups = groups

    # -------------------------------
    # ROLE VALIDATIONS
    # -------------------------------

    def validate_role_inheritance(self):
        """Ensure parent roles exist."""
        for role_name, role in self.roles.items():
            if role.parent_role and role.parent_role.name not in self.roles:
                self.add_error(
                    None,
                    f"Role '{role_name}' (line {role.line_number}) "
                    f"extends undefined role '{role.parent_role.name}'"
                )

    def detect_circular_inheritance(self):
        """Detect cycles in role inheritance."""
        visited = set()
        stack = set()
        path = []

        def dfs(role_name: str):
            visited.add(role_name)
            stack.add(role_name)
            path.append(role_name)

            role = self.roles[role_name]
            parent = role.parent_role

            if parent:
                parent_name = parent.name

                if parent_name not in visited:
                    dfs(parent_name)

                elif parent_name in stack:
                    cycle_start = path.index(parent_name)
                    cycle = path[cycle_start:] + [parent_name]
                    self.add_error(None, f"Circular inheritance detected: {' → '.join(cycle)}")

            path.pop()
            stack.remove(role_name)

        for role_name in self.roles:
            if role_name not in visited:
                path.clear()
                dfs(role_name)

    # -------------------------------
    # USER VALIDATIONS
    # -------------------------------

    def validate_user_roles(self):
        """Ensure users only reference valid roles."""
        for user_name, user in self.users.items():
            for role in user.roles:
                if role.name not in self.roles:
                    self.add_error(
                        None,
                        f"User '{user_name}' (line {user.line_number}) "
                        f"references undefined role '{role.name}'"
                    )

    # -------------------------------
    # GROUP VALIDATIONS
    # -------------------------------

    def validate_group_members(self):
        """Ensure group users and roles exist."""
        for group_name, group in self.groups.items():

            for member in group.members:
                if member not in self.users:
                    self.add_warning(
                        None,
                        f"Group '{group_name}' (line {group.line_number}) "
                        f"references undefined user '{member}'"
                    )

            for role_name in group.roles:
                if role_name not in self.roles:
                    self.add_error(
                        None,
                        f"Group '{group_name}' (line {group.line_number}) "
                        f"references undefined role '{role_name}'"
                    )

    # -------------------------------
    # PERMISSIONS
    # -------------------------------

    def get_user_permissions(self, user_name: str) -> List[PermissionBlock]:
        """Resolve all permissions for a user."""
        if user_name not in self.users:
            return []

        user = self.users[user_name]
        return user.get_all_permissions(self.roles)

    def get_role_hierarchy(self, role_name: str) -> List[str]:
        """Return inheritance chain for role."""
        if role_name not in self.roles:
            return []

        hierarchy = []
        current = self.roles[role_name]

        while current:
            hierarchy.append(current.name)
            if not current.parent_role:
                break
            current = self.roles.get(current.parent_role.name)

        return hierarchy

    # -------------------------------
    # ERROR HANDLING
    # -------------------------------

    @staticmethod
    def get_line_column(ctx):
        if ctx:
            return ctx.start.line, ctx.start.column
        return 0, 0

    def add_error(self, ctx, message: str):
        line, column = self.get_line_column(ctx)
        self.errors.append(ErrorResponse(
            message=message,
            line_number=line,
            column_number=column
        ))

    def add_warning(self, ctx, message: str):
        line, column = self.get_line_column(ctx)
        self.warnings.append(WarningResponse(
            message=message,
            line_number=line,
            column_number=column
        ))

    # -------------------------------
    # MASTER DISPATCHER
    # -------------------------------

    def run_all(self):
        """Run every semantic validation."""
        self.validate_role_inheritance()
        self.detect_circular_inheritance()
        self.validate_user_roles()
        self.validate_group_members()

