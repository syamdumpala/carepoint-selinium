from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "config.ini"


def read_config() -> ConfigParser:
    parser = ConfigParser()
    if not parser.read(CONFIG_PATH):
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_PATH}")
    return parser


CONFIG = read_config()
