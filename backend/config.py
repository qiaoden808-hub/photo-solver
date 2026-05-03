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
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

_lock = threading.Lock()


def _load_settings():
    """Load from settings.json, with env var overrides."""
    cfg = {"api_key": "", "model": "gemini-3-flash-preview"}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                cfg.update(json.load(f))
        except Exception:
            pass
    # Env vars override settings.json (used for Vercel deployment)
    if os.environ.get("API_KEY"):
        cfg["api_key"] = os.environ["API_KEY"]
    if os.environ.get("MODEL"):
        cfg["model"] = os.environ["MODEL"]
    cfg.setdefault("endpoint", "https://api.openai.com/v1")
    return cfg


_default_config = _load_settings()
_config: dict = {}


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_from_disk():
    global _config
    _ensure_data_dir()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                _config = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load config file: {e}")
            _config = {}
    else:
        _config = {}


def _save_to_disk():
    _ensure_data_dir()
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(_config, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"Error: Failed to save config file: {e}")


def get_config() -> dict:
    with _lock:
        cfg = _config if _config else _default_config
        api_key = cfg.get("api_key", "")
        masked_key = api_key[:4] + "****" if api_key else ""
        return {
            "api_key": masked_key,
            "endpoint": cfg.get("endpoint", _default_config["endpoint"]),
            "model": cfg.get("model", _default_config["model"]),
        }


def save_config(api_config: ApiConfig) -> dict:
    with _lock:
        _config["api_key"] = api_config.api_key
        _config["endpoint"] = api_config.endpoint or _default_config["endpoint"]
        _config["model"] = api_config.model or _default_config["model"]
        _save_to_disk()
        return {"status": "ok"}


def get_api_key() -> str:
    cfg = _config if _config else _default_config
    return cfg.get("api_key", "")


def get_endpoint() -> str:
    cfg = _config if _config else _default_config
    return cfg.get("endpoint", _default_config["endpoint"])


def get_model() -> str:
    cfg = _config if _config else _default_config
    return cfg.get("model", _default_config["model"])
