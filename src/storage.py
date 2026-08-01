"""
Simple storage layer.

The assignment says storage can be "in memory or a local JSON file — no
database required". We use a JSON file (expenses_data.json) so that data
survives a server restart, but the whole thing is still just a plain
Python list of dicts under the hood - easy to read and reason about.

Keeping this logic in its own file (separate from main.py, which handles
HTTP/routing) is a common good practice called "separation of concerns":
if we ever swap JSON-file storage for a real database, only this file
needs to change.
"""

import json
import os
from threading import Lock
from typing import List, Dict

# Where we keep the data. Using an absolute path based on this file's
# location so it works no matter which folder you run the server from.
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "expenses_data.json")

# A lock to avoid two requests corrupting the file if they write at the
# exact same time (unlikely in this small app, but it's good practice).
_lock = Lock()


def _read_all() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)


def _write_all(expenses: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2, default=str)


def get_all() -> List[Dict]:
    with _lock:
        return _read_all()


def add(expense: Dict) -> Dict:
    with _lock:
        expenses = _read_all()
        expenses.append(expense)
        _write_all(expenses)
        return expense


def delete(expense_id: int) -> bool:
    """Returns True if something was deleted, False if id was not found."""
    with _lock:
        expenses = _read_all()
        new_expenses = [e for e in expenses if e["id"] != expense_id]
        if len(new_expenses) == len(expenses):
            return False
        _write_all(new_expenses)
        return True


def next_id() -> int:
    with _lock:
        expenses = _read_all()
        if not expenses:
            return 1
        return max(e["id"] for e in expenses) + 1


def clear_all() -> None:
    """Used by tests to reset state between test runs."""
    with _lock:
        _write_all([])
