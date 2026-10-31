from __future__ import annotations

import os
import platform
import re
import base64
from pathlib import Path

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from utilities.logger import configure_logging
from utilities.screenshot_helper import save_screenshot

load_dotenv()

ROOT = Path(__file__).parent
SCREENSHOTS = ROOT / "artifacts" / "screenshots"
LOG_PATH = ROOT / "artifacts" / "logs" / "execution.log"


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("carepoint")
    group.addoption("--browser", choices=("chrome", "edge"), default=os.getenv("BROWSER", "chrome"))
    group.addoption("--headless", action="store_true", default=os.getenv("HEADLESS", "true").lower() == "true")
    group.addoption("--headed", action="store_true", help="Override configured headless mode")
    group.addoption(
        "--base-url",
        default=os.getenv("CAREPOINT_BASE_URL", "https://www.qapractice.com/practice-forms"),
    )


def _build_driver(browser: str, headless: bool) -> webdriver.Remote:
    if browser == "chrome":
        options = ChromeOptions()
    else:
        options = EdgeOptions()
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-notifications")
    if headless:
        options.add_argument("--headless=new")
    return webdriver.Chrome(options=options) if browser == "chrome" else webdriver.Edge(options=options)


def pytest_configure(config: pytest.Config) -> None:
    try:
        from pytest_metadata.plugin import metadata_key

        metadata = config.stash[metadata_key]
        metadata["Python"] = platform.python_version()
        metadata["Platform"] = platform.platform()
        metadata["Browser"] = config.getoption("--browser")
        metadata["Base URL"] = config.getoption("--base-url")
        metadata["Project"] = "CarePoint Clinic Form UI Automation"
    except ImportError:
        pass


@pytest.fixture(scope="session")
def base_url(request: pytest.FixtureRequest) -> str:
    return request.config.getoption("--base-url")


@pytest.fixture
def driver(request: pytest.FixtureRequest) -> webdriver.Remote:
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless") and not request.config.getoption("--headed")
    browser_driver = _build_driver(browser, headless)
    browser_driver.set_page_load_timeout(int(os.getenv("PAGE_LOAD_TIMEOUT", "30")))
    yield browser_driver
    browser_driver.quit()


@pytest.fixture(autouse=True)
def test_logging() -> None:
    configure_logging(LOG_PATH)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    browser_driver = item.funcargs.get("driver")
    if browser_driver is None:
        return
    test_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", item.nodeid)
    screenshot_path = SCREENSHOTS / f"{test_id}.png"
    if save_screenshot(browser_driver, screenshot_path):
        try:
            import pytest_html

            report.extras = getattr(report, "extras", [])
            encoded = base64.b64encode(screenshot_path.read_bytes()).decode("ascii")
            report.extras.append(pytest_html.extras.image(encoded, mime_type="image/png"))
        except ImportError:
            pass
