from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class User:
    username: str
    password: str
    role: str


class AuthService:
    def __init__(self) -> None:
        self._users: Dict[str, User] = {}
        self._sessions: List[str] = []

    def register(self, username: str, password: str, role: str) -> User:
        user = User(username=username, password=password, role=role)
        self._users[username] = user
        return user

    def authenticate(self, username: str, password: str) -> User | None:
        user = self._users.get(username)
        if user and user.password == password:
            return user
        return None

    def create_session(self, username: str) -> str:
        self._sessions.append(username)
        return username

    def is_authorized(self, username: str, required_role: str) -> bool:
        user = self._users.get(username)
        if user is None:
            return False
        role_priority = {"cashier": 1, "manager": 2, "owner": 3}
        return role_priority.get(user.role, 0) >= role_priority.get(required_role, 0)
