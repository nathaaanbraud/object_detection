import json
import os
from typing import Any, Dict

CONFIG_FILE = 'config.json'


def load_config(config_file: str = CONFIG_FILE) -> Dict[str, Any]:
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config


def get_video_path(config: Dict[str, Any]) -> str:
    config_video = config.get('videos', {})
    return config_video.get('path', '')
