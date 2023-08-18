from pathlib import Path
from typing import Any, Optional

import toml

from .report import Report


class Config:
    def __init__(self, report: Report) -> None:
        # read configuration file
        config_file = Path("config.toml")
        if config_file.exists():
            report.info("Found configuration file.", path=config_file)
            self.config = toml.load(config_file)
            if "replacements" in self.config:
                self.replacements = self.config["replacements"]
        else:
            self.config = None
            self.replacements = {}

    def has_config(self, key: str) -> bool:
        return self.config is not None and key in self.config

    def get(self, key: str) -> Optional[Any]:
        return (
            self.config[key] if self.config is not None and key in self.config else None
        )

    def get_replacement(self, variable: str) -> Optional[str]:
        return self.replacements.get(variable, None)
