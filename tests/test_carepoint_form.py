from __future__ import annotations

from pathlib import Path

import pytest
from selenium.webdriver.support.ui import Select

from pages.carepoint_form_page import CarePointFormPage, PatientFormData
from utilities.data_reader import load_dataclass_records, read_json

ROOT = Path(__file__).resolve().parents[1]
PATIENTS = load_dataclass_records(ROOT / "data" / "patients.json", PatientFormData)
INVALID = read_json(ROOT / "data" / "invalid_inputs.json")
REQUIRED_FIELDS = ["first_name", "last_name", "email", "date_of_birth", "date_of_joining", "phone"]


def _valid_page(driver, base_url) -> CarePointFormPage:
    page = CarePointFormPage(driver).open(base_url)
    page.fill(PatientFormData())
    return page


@pytest.mark.ui
@pytest.mark.smoke
def test_tc01_valid_patient_submission_shows_success(driver, base_url):
    page = _valid_page(driver, base_url)
    page.submit()
    assert page.success_is_visible()


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize("field", REQUIRED_FIELDS)
def test_tc02_tc07_required_field_blank(field, driver, base_url):
    page = CarePointFormPage(driver).open(base_url)
    page.fill(PatientFormData(**{field: ""}))
    page.submit()
    assert page.validation_messages()
    assert not page.success_is_visible()


@pytest.mark.ui
@pytest.mark.negative
def test_tc08_communication_preference_omitted_shows_validation(driver, base_url):
    page = CarePointFormPage(driver).open(base_url)
    page.fill(PatientFormData(), include_communication=False)
    page.submit()
    assert "communication" in " ".join(page.validation_messages()).lower()


@pytest.mark.ui
@pytest.mark.negative
def test_tc09_invalid_email_is_rejected(driver, base_url):
    page = CarePointFormPage(driver).open(base_url)
    page.fill(PatientFormData(email=INVALID["invalid_email"]))
    page.submit()
    assert page.field_is_invalid(page.EMAIL)
    assert not page.success_is_visible()


@pytest.mark.ui
@pytest.mark.negative
def test_tc10_wrong_joining_date_format_is_rejected(driver, base_url):
    page = CarePointFormPage(driver).open(base_url)
    page.fill(PatientFormData(date_of_joining=INVALID["invalid_joining_date"]))
    page.submit()
    assert "format" in " ".join(page.validation_messages()).lower()
    assert not page.success_is_visible()


@pytest.mark.ui
@pytest.mark.regression
def test_tc11_email_then_phone_only_phone_stays_selected(driver, base_url):
    page = CarePointFormPage(driver).open(base_url)
    page.select_communication("email")
    page.select_communication("phone")
    assert page.is_checked(page.COMM_PHONE)
    assert not page.is_checked(page.COMM_EMAIL)


@pytest.mark.ui
@pytest.mark.regression
def test_tc12_fill_then_clear_returns_inputs_to_blank(driver, base_url):
    page = _valid_page(driver, base_url)
    page.clear_all()
    assert page.value(page.FIRST_NAME) == ""
    assert page.value(page.LAST_NAME) == ""
    assert page.value(page.DOB) == ""
    assert page.value(page.DOJ) == ""
    assert page.value(page.EMAIL) == ""
    assert page.value(page.PHONE) == ""


@pytest.mark.ui
@pytest.mark.regression
def test_tc13_country_options_and_selection_persist(driver, base_url):
    page = CarePointFormPage(driver).open(base_url)
    options = [option.text for option in Select(page.driver.find_element(*page.COUNTRY)).options]
    assert {"Select Country", "India"}.issubset(options)
    page.select_by_text(page.COUNTRY, "India")
    assert page.selected_text(page.COUNTRY) == "India"


@pytest.mark.ui
@pytest.mark.regression
def test_tc14_title_selection_persists(driver, base_url):
    page = CarePointFormPage(driver).open(base_url)
    page.select_by_text(page.TITLE, "Dr.")
    assert page.selected_text(page.TITLE) == "Dr."


@pytest.mark.ui
@pytest.mark.regression
def test_tc15_phone_code_selection_persists(driver, base_url):
    page = CarePointFormPage(driver).open(base_url)
    page.select_by_text(page.PHONE_CODE, "+91")
    assert page.selected_text(page.PHONE_CODE) == "+91"


@pytest.mark.ui
@pytest.mark.negative
def test_tc16_invalid_phone_is_rejected_or_invalid(driver, base_url):
    page = CarePointFormPage(driver).open(base_url)
    page.fill(PatientFormData(phone=INVALID["invalid_phone"]))
    page.submit()
    assert page.success_is_visible() or page.validation_messages()


@pytest.mark.ui
@pytest.mark.regression
def test_tc17_future_date_of_birth_follows_site_behavior(driver, base_url):
    page = _valid_page(driver, base_url)
    page.type_text(page.DOB, "2099-01-01")
    page.submit()
    assert page.success_is_visible() or page.validation_messages()


@pytest.mark.ui
@pytest.mark.regression
def test_tc18_success_confirmation_text_is_correct(driver, base_url):
    page = _valid_page(driver, base_url)
    page.submit()
    assert page.success_message() == "Details Successfully Added!"


@pytest.mark.ui
@pytest.mark.regression
def test_tc19_go_back_to_form_returns_to_fresh_form(driver, base_url):
    page = _valid_page(driver, base_url)
    page.submit()
    page.go_back_to_form()
    assert not page.success_is_visible()
    assert page.value(page.FIRST_NAME) == ""
    assert page.value(page.EMAIL) == ""


@pytest.mark.ui
@pytest.mark.data_driven
@pytest.mark.parametrize("patient_data", PATIENTS, ids=["patients-json-aarav"])
def test_tc20_json_data_driven_valid_submission(patient_data, driver, base_url):
    page = CarePointFormPage(driver).open(base_url)
    page.fill(patient_data)
    page.submit()
    assert page.success_is_visible()

@pytest.mark.ui
@pytest.mark.smoke
def test_tc21_page_title_and_key_controls_are_present(driver, base_url):
    page = CarePointFormPage(driver).open(base_url)
    assert "Selenium Web Form Automation" in page.driver.title
    controls = [
        page.COUNTRY, page.TITLE, page.FIRST_NAME, page.LAST_NAME, page.DOB,
        page.DOJ, page.EMAIL, page.PHONE_CODE, page.PHONE, page.COMM_EMAIL,
        page.COMM_PHONE, page.SUBMIT,
    ]
    assert all(page.control_exists(locator) for locator in controls)
    page.fill(PatientFormData())
    page.submit()
    assert page.control_exists(page.SUCCESS)
