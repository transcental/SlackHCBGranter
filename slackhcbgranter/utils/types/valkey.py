from dataclasses import dataclass
from typing import Literal
from typing import Optional


@dataclass
class OrgUser:
    id: str
    role: Literal["member", "manager"]


@dataclass
class Organisation:
    id: str
    name: str
    slug: str
    balance: float
    users: list[OrgUser]
    playground_mode: bool
    icon: Optional[str]
    expiresAt: str


@dataclass
class User:
    id: str
    name: str
    email: str
    avatar: str
    admin: bool
    expiresAt: str
    token: str
    organisations: list[str]
