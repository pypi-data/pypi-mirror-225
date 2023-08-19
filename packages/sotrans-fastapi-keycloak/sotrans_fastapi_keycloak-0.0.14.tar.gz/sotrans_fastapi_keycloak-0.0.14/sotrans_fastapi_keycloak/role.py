class Role:
    def __init__(self, ancestors: list['Role'] | None = None):
        """Role class constructor

        Args:
            ancestors: ancestor roles with lower access level
        """
        if ancestors is None:
            ancestors = []

        self.ancestors = ancestors

    def check_access(self, required_role: 'Role') -> bool:
        """Check if current role satisfies access level of required role

        Args:
            required_role: role, to check if access level of current role is equal or better in hierarchy tree

        Returns: result of checking access level
        """
        return Role._check_access(required_role, self)

    @staticmethod
    def _check_access(required_role: 'Role', current_role: 'Role') -> bool:
        if current_role is required_role:
            return True
        for current_role_ancestor in current_role.ancestors:
            if Role._check_access(required_role, current_role_ancestor):
                return True
        return False
