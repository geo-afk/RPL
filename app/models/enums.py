from enum import Enum

class PolicyEffect(Enum):
    ALLOW = "allow"
    DENY = "deny"


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    MODIFY = "modify"
    START = "start"
    STOP = "stop"
    DEPLOY = "deploy"
    DELETE = "delete"
    EXECUTE = "execute"
    ALL = "*"

