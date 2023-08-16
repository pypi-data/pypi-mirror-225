from __future__ import annotations

__all__ = ["Issue"]

from .base import Base, field


class Issue(Base, kw_only=True, frozen=True):
    """Represents short view of issue."""

    url: str = field(name="self")
    id: str
    key: str
    display: str
