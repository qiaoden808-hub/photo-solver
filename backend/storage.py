import json
import os
import threading
from datetime import datetime
from typing import Optional

if os.environ.get("VERCEL"):
    DATA_DIR = "/tmp/data"
else:
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

_lock = threading.Lock()
_records: dict[str, dict] = {}


def _ensure_data_dir():
    """Ensure the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_from_disk():
    """Load all records from the JSON file into memory."""
    global _records
    _ensure_data_dir()
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    _records = {r["id"]: r for r in data}
                else:
                    _records = {}
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load history file: {e}")
            _records = {}
    else:
        _records = {}


def _save_to_disk():
    """Save all in-memory records to the JSON file."""
    _ensure_data_dir()
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(list(_records.values()), f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"Error: Failed to save history file: {e}")


def save(record: dict) -> dict:
    """Save a solve record.

    The record must have an 'id' key.
    Returns the saved record.
    """
    global _records
    with _lock:
        _records[record["id"]] = record
        _save_to_disk()
        return record


def get_all() -> list[dict]:
    """Get all history records, sorted by created_at descending.

    Returns only summary fields (no full solution content).
    """
    with _lock:
        if not _records:
            _load_from_disk()
        records = list(_records.values())
        records.sort(key=lambda r: r.get("created_at", ""), reverse=True)
        return [
            {
                "id": r["id"],
                "problem": r["problem"],
                "subject": r["subject"],
                "created_at": r["created_at"],
            }
            for r in records
        ]


def get_by_id(record_id: str) -> Optional[dict]:
    """Get a single record by its ID, including full solution."""
    with _lock:
        if not _records:
            _load_from_disk()
        return _records.get(record_id)


def delete(record_id: str) -> bool:
    """Delete a record by its ID.

    Returns True if deleted, False if not found.
    """
    with _lock:
        if not _records:
            _load_from_disk()
        if record_id in _records:
            del _records[record_id]
            _save_to_disk()
            return True
        return False


# Initialize on module import
_load_from_disk()
