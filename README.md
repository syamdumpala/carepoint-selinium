# CarePoint Form Automation

Advanced Selenium WebDriver automation for the CarePoint-style web form at
`https://www.qapractice.com/practice-forms`.

## Highlights

- Page Object Model with a reusable wait and interaction layer.
- Chrome and Edge support through `--browser`.
- Headless execution for CI, explicit waits, screenshots, structured logging,
  HTML and JUnit XML reports.
- Data-driven valid and invalid scenarios.
- Positive workflow, required-field validation, communication validation,
  radio-button exclusivity, reset behavior, email validation, and date validation.
- GitHub Actions Chrome/Edge browser matrix with uploaded HTML, JUnit and
  failure evidence.
- Automatic Selenium Manager driver resolution; no checked-in browser drivers.

## Setup and execution

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
pytest --browser chrome --headless
pytest --browser chrome --headed -m "smoke or negative"
pytest --browser edge --headless
python generate_report.py
```

Reports are written to `reports/`, screenshots to `artifacts/screenshots/`, and
logs to `artifacts/logs/`. Use `py generate_report.py` to create the academic
PDF report after execution.

Only dummy data is used. The practice site states that submitted data is not
stored.

## Assessment evidence

The suite covers the valid workflow, six required-field scenarios, missing
communication preference, invalid email, invalid date-of-joining format,
radio-button exclusivity, and reset behavior. CI runs the same suite against
Chrome and Edge. The academic report in `reports/CarePoint_Project_Report.pdf`
documents the workflow, locator inventory, architecture, synchronization,
execution evidence, source-code responsibilities, checklist compliance and
future enhancements.
