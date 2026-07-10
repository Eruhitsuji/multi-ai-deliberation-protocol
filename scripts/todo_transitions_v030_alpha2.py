#!/usr/bin/env python3
from __future__ import annotations

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "OPEN": {"IN_PROGRESS", "BLOCKED", "DEFERRED", "CANCELLED"},
    "IN_PROGRESS": {"BLOCKED", "DONE", "DEFERRED", "CANCELLED"},
    "BLOCKED": {"IN_PROGRESS", "DEFERRED", "CANCELLED"},
    "DEFERRED": {"OPEN", "IN_PROGRESS", "CANCELLED"},
    "DONE": set(),
    "CANCELLED": set(),
}

TERMINAL_STATUSES = {"DONE", "CANCELLED"}


def transition_allowed(old: str, new: str) -> bool:
    return new in ALLOWED_TRANSITIONS.get(old, set())
