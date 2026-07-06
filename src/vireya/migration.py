from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class MigrationIssue:
    message: str


@dataclass
class MigrationImport:
    source_file: str
    issues: List[MigrationIssue] = field(default_factory=list)
    audit_log: List[MigrationIssue] = field(default_factory=list)

    def validate_row(self, row: Dict[str, Any]) -> None:
        if not row.get("id") or not row.get("name"):
            self.issues.append(MigrationIssue("invalid row"))

    def mark_issue(self, message: str) -> None:
        self.audit_log.append(MigrationIssue(message))
