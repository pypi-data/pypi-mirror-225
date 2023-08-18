from enum import Enum


class DeleteDraftKind(str, Enum):
    SCRIPT = "script"
    FLOW = "flow"
    APP = "app"

    def __str__(self) -> str:
        return str(self.value)
