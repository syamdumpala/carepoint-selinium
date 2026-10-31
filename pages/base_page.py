from __future__ import annotations

import logging
import os
from typing import Callable, TypeVar

from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

T = TypeVar("T")


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.wait = WebDriverWait(
            driver,
            int(os.getenv("EXPLICIT_WAIT", "15")),
            ignored_exceptions=(StaleElementReferenceException,),
        )

    def locator(self, css_selector: str) -> tuple[str, str]:
        return (By.CSS_SELECTOR, css_selector)

    def wait_for_visible(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: tuple[str, str]) -> None:
        element = self.wait_for_clickable(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator: tuple[str, str], text: str) -> None:
        element = self.wait_for_visible(locator)
        element.clear()
        element.send_keys(text)

    def select_by_text(self, locator: tuple[str, str], text: str) -> None:
        Select(self.wait_for_visible(locator)).select_by_visible_text(text)

    def select_radio(self, locator: tuple[str, str]) -> None:
        self.click(locator)

    def get_validation_message(self, locator: tuple[str, str]) -> str:
        return self.wait_for_visible(locator).get_attribute("validationMessage") or ""

    def take_screenshot(self, output_path: str) -> bool:
        return self.driver.save_screenshot(output_path)

    def value(self, locator: tuple[str, str]) -> str:
        return self.wait_for_visible(locator).get_attribute("value") or ""

    def wait_for(self, condition: Callable[[WebDriver], T]) -> T:
        return self.wait.until(condition)
