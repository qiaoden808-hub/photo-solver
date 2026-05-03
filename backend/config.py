import json
import os
import threading

from models import ApiConfig

# Vercel filesystem is read-only, use /tmp for data
if os.environ.get("VERCEL"):
    DATA_DIR = "/tmp/data"
else:
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

_lock = threading.Lock()

# Default configuration
_default_config = {
    "api_key": "",
    "endpoint": "https://api.openai.com/v1",
    "model": "gpt-4o",
}

_config: dict = {}


def _ensure_data_dir():
    """Ensure the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_from_disk():
    """Load config from the JSON file into memory."""
    global _config
    _ensure_data_dir()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                _config = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load config file: {e}")
            _config = {}
    else:
        _config = {}


def _save_to_disk():
    """Save current config to disk."""
    _ensure_data_dir()
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(_config, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"Error: Failed to save config file: {e}")


def get_config() -> dict:
    """Get the current configuration with masked API key."""
    with _lock:
        if not _config:
            _load_from_disk()
        api_key = _config.get("api_key", _default_config["api_key"])
        masked_key = ""
        if api_key:
            masked_key = api_key[:4] + "****"
        return {
            "api_key": masked_key,
            "endpoint": _config.get("endpoint", _default_config["endpoint"]),
            "model": _config.get("model", _default_config["model"]),
        }


def save_config(api_config: ApiConfig) -> dict:
    """Save API configuration to disk."""
    with _lock:
        _config["api_key"] = api_config.api_key
        _config["endpoint"] = api_config.endpoint or _default_config["endpoint"]
        _config["model"] = api_config.model or _default_config["model"]
        _save_to_disk()
        return {"status": "ok"}


def get_api_key() -> str:
    """Get the full API key for internal use."""
    with _lock:
        if not _config:
            _load_from_disk()
        return _config.get("api_key", "")


def get_endpoint() -> str:
    """Get the API endpoint."""
    with _lock:
        if not _config:
            _load_from_disk()
        return _config.get("endpoint", _default_config["endpoint"])


def get_model() -> str:
    """Get the model name."""
    with _lock:
        if not _config:
            _load_from_disk()
        return _config.get("model", _default_config["model"])


# Initialize on module import
_load_from_disk()
