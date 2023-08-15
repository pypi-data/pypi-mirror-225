from enum import Enum


class RawScriptLanguage(str, Enum):
    DENO = "deno"
    BUN = "bun"
    PYTHON3 = "python3"
    GO = "go"
    BASH = "bash"
    POWERSHELL = "powershell"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    BIGQUERY = "bigquery"
    SNOWFLAKE = "snowflake"
    GRAPHQL = "graphql"
    NATIVETS = "nativets"

    def __str__(self) -> str:
        return str(self.value)
