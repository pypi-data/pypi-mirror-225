from enum import Enum


class NewScriptWithDraftDraftKind(str, Enum):
    SCRIPT = "script"
    FAILURE = "failure"
    TRIGGER = "trigger"
    COMMAND = "command"
    APPROVAL = "approval"

    def __str__(self) -> str:
        return str(self.value)
