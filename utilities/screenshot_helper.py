from __future__ import annotations

import logging
from pathlib import Path

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver


def save_screenshot(driver: WebDriver, output_path: Path) -> bool:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        return driver.save_screenshot(str(output_path))
    except WebDriverException as exc:
        logging.getLogger(__name__).warning("Screenshot unavailable: %s", exc)
        return False
