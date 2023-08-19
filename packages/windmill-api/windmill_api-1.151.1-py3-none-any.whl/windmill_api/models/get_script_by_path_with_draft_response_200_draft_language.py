from enum import Enum


class GetScriptByPathWithDraftResponse200DraftLanguage(str, Enum):
    PYTHON3 = "python3"
    DENO = "deno"
    GO = "go"
    BASH = "bash"
    POWERSHELL = "powershell"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    BIGQUERY = "bigquery"
    SNOWFLAKE = "snowflake"
    GRAPHQL = "graphql"
    NATIVETS = "nativets"
    BUN = "bun"

    def __str__(self) -> str:
        return str(self.value)
