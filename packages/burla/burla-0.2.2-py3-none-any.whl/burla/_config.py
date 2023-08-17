import json
import appdirs
from pathlib import Path
from typing import Tuple

CONFIG_DIR = Path(appdirs.user_config_dir(appname="burla", appauthor="burla"))
CONFIG_PATH = CONFIG_DIR / Path("burla_config.json")


def set_api_key(api_key: str):
    """
    API_KEY: Email jake@burla.dev to get an API key!
    """
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.touch()
    CONFIG_PATH.write_text(json.dumps({"API_KEY": api_key}))


def load_api_key_from_local_config() -> Tuple[str, str]:
    if not CONFIG_PATH.exists():
        raise Exception(
            (
                "No API key found.\n"
                "To set an API key run: `burla set_api_key <your API key>`\n"
                "To request an API key email jake@burla.dev."
            )
        )
    config = json.loads(CONFIG_PATH.read_text())
    return config["API_KEY"]
