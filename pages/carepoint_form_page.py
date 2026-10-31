from __future__ import annotations

from dataclasses import dataclass

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


@dataclass(frozen=True)
class PatientFormData:
    first_name: str = "Aarav"
    last_name: str = "Sharma"
    email: str = "aarav.sharma@example.test"
    date_of_birth: str = "1995-08-15"
    date_of_joining: str = "01/06/2021"
    phone: str = "9876543210"
    country: str = "India"
    title: str = "Dr."
    phone_code: str = "+91"
    communication: str = "email"


class CarePointFormPage(BasePage):
    URL = "https://www.qapractice.com/practice-forms"

    COUNTRY = (By.ID, "forms-country")
    TITLE = (By.ID, "forms-title")
    FIRST_NAME = (By.ID, "forms-first-name")
    LAST_NAME = (By.ID, "forms-last-name")
    DOB = (By.ID, "forms-dob")
    DOJ = (By.ID, "forms-doj")
    EMAIL = (By.ID, "forms-email")
    PHONE_CODE = (By.ID, "forms-phone-code")
    PHONE = (By.ID, "forms-phone-number")
    COMM_EMAIL = (By.ID, "forms-comm-email")
    COMM_PHONE = (By.ID, "forms-comm-phone")
    SUBMIT = (By.ID, "forms-submit")
    CLEAR = (By.ID, "forms-clear")
    SUCCESS = (By.ID, "forms-success")
    GO_BACK = (By.XPATH, "//button[contains(., 'Go Back to Form')]")

    def open(self, url: str = URL) -> "CarePointFormPage":
        self.driver.get(url)
        self.wait_for_visible(self.FIRST_NAME)
        return self

    def fill(self, data: PatientFormData = PatientFormData(), *, include_communication: bool = True) -> None:
        for locator, value in (
            (self.FIRST_NAME, data.first_name),
            (self.LAST_NAME, data.last_name),
            (self.DOB, data.date_of_birth),
            (self.DOJ, data.date_of_joining),
            (self.EMAIL, data.email),
            (self.PHONE, data.phone),
        ):
            self.type_text(locator, value)
        for locator, value in (
            (self.COUNTRY, data.country),
            (self.TITLE, data.title),
            (self.PHONE_CODE, data.phone_code),
        ):
            self.select_by_text(locator, value)
        if include_communication:
            self.select_communication(data.communication)

    def submit(self) -> None:
        self.click(self.SUBMIT)

    def select_communication(self, preference: str) -> None:
        self.select_radio(self.COMM_EMAIL if preference.lower() == "email" else self.COMM_PHONE)

    def success_is_visible(self) -> bool:
        elements = self.driver.find_elements(*self.SUCCESS)
        return bool(elements and elements[0].is_displayed())

    def success_message(self) -> str:
        return self.wait_for_visible(self.SUCCESS).text

    def validation_messages(self) -> list[str]:
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".text-danger, [role='alert']")
        return [element.text for element in elements if element.is_displayed() and element.text]

    def field_is_invalid(self, locator: tuple[str, str]) -> bool:
        element = self.wait_for_visible(locator)
        return not bool(self.driver.execute_script("return arguments[0].checkValidity();", element))

    def clear_all(self) -> None:
        self.click(self.CLEAR)

    def go_back_to_form(self) -> None:
        self.click(self.GO_BACK)
        self.wait_for_visible(self.FIRST_NAME)

    def selected_text(self, locator: tuple[str, str]) -> str:
        return Select(self.wait_for_visible(locator)).first_selected_option.text

    def is_checked(self, locator: tuple[str, str]) -> bool:
        return self.wait_for_visible(locator).is_selected()

    def control_exists(self, locator: tuple[str, str]) -> bool:
        return bool(self.driver.find_elements(*locator))
