from __future__ import annotations

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

ROOT = Path(__file__).parent
OUTPUT = ROOT / "artifacts" / "working_screenshots"
OUTPUT.mkdir(parents=True, exist_ok=True)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1440,1000")
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.qapractice.com/practice-forms")
    driver.save_screenshot(str(OUTPUT / "01_form_initial.png"))

    Select(driver.find_element("id", "forms-country")).select_by_visible_text("India")
    Select(driver.find_element("id", "forms-title")).select_by_visible_text("Dr.")
    driver.find_element("id", "forms-first-name").send_keys("Aarav")
    driver.find_element("id", "forms-last-name").send_keys("Sharma")
    driver.find_element("id", "forms-dob").send_keys("1995-08-15")
    driver.find_element("id", "forms-doj").send_keys("01/06/2021")
    driver.find_element("id", "forms-email").send_keys("aarav.sharma@example.test")
    Select(driver.find_element("id", "forms-phone-code")).select_by_visible_text("+91")
    driver.find_element("id", "forms-phone-number").send_keys("9876543210")
    driver.find_element("id", "forms-comm-email").click()
    driver.save_screenshot(str(OUTPUT / "02_form_completed.png"))

    driver.find_element("id", "forms-submit").click()
    driver.save_screenshot(str(OUTPUT / "03_submission_success.png"))
finally:
    driver.quit()

print(OUTPUT)
