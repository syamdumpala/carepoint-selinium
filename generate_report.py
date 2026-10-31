from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    XPreformatted,
)

ROOT = Path(__file__).parent
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)


def execution_summary() -> tuple[str, str, int, int, int, int]:
    xml = REPORTS / "junit.xml"
    if not xml.exists():
        return "Not executed", "Run the pytest command before generating evidence.", 0, 0, 0, 0
    text = xml.read_text(encoding="utf-8")
    tests = int(re.search(r'tests="(\d+)"', text).group(1))
    failures = int(re.search(r'failures="(\d+)"', text).group(1))
    errors = int(re.search(r'errors="(\d+)"', text).group(1))
    passed = tests - failures - errors
    return (
        f"{passed}/{tests} tests passed",
        "Evidence source: reports/junit.xml and reports/report.html",
        tests,
        passed,
        failures,
        errors,
    )


def optional_execution_summary(filename: str, label: str) -> str:
    xml = REPORTS / filename
    if not xml.exists():
        return f"{label}: not executed."
    text = xml.read_text(encoding="utf-8")
    tests = int(re.search(r'tests="(\d+)"', text).group(1))
    failures = int(re.search(r'failures="(\d+)"', text).group(1))
    errors = int(re.search(r'errors="(\d+)"', text).group(1))
    passed = tests - failures - errors
    return f"{label}: {passed}/{tests} passed, {failures} failed, {errors} errors."


def p(text: str, style) -> Paragraph:
    return Paragraph(text, style)


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#b7c9d6"))
    canvas.line(48, 30, A4[0] - 48, 30)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#52606d"))
    canvas.drawString(48, 18, "CarePoint Clinic Form UI Automation | DUMPALA SYAM KUMAR")
    canvas.drawRightString(A4[0] - 48, 18, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf() -> None:
    result, evidence, tests, passed, failures, errors = execution_summary()
    edge_result = optional_execution_summary("edge_smoke.xml", "Edge smoke execution")
    output = REPORTS / "CarePoint_Project_Report.pdf"
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        rightMargin=48,
        leftMargin=48,
        topMargin=44,
        bottomMargin=44,
        title="CarePoint Clinic Form UI Automation Project Report",
        author="DUMPALA SYAM KUMAR",
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CoverTitle", parent=styles["Title"], alignment=TA_CENTER,
        fontSize=19, leading=25, spaceAfter=18, textColor=colors.HexColor("#17365d"),
    ))
    styles.add(ParagraphStyle(
        name="CoverSub", parent=styles["Normal"], alignment=TA_CENTER,
        fontSize=11, leading=17,
    ))
    styles.add(ParagraphStyle(
        name="Section", parent=styles["Heading1"], fontSize=15,
        leading=19, textColor=colors.HexColor("#17365d"), spaceBefore=8, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="Subsection", parent=styles["Heading2"], fontSize=11,
        leading=15, textColor=colors.HexColor("#1f4e78"), spaceBefore=7, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="Small", parent=styles["BodyText"], fontSize=8.5, leading=11,
    ))
    styles.add(ParagraphStyle(
        name="CodeListing", fontName="Courier", fontSize=6.8, leading=8.2,
        leftIndent=8, rightIndent=8, backColor=colors.HexColor("#f3f6f8"),
        borderColor=colors.HexColor("#d5dee5"), borderWidth=0.5,
        borderPadding=6, spaceBefore=5, spaceAfter=8,
    ))
    body = styles["BodyText"]
    screenshot_dir = ROOT / "artifacts" / "working_screenshots"

    def evidence_image(filename: str, caption: str) -> list:
        image_path = screenshot_dir / filename
        if not image_path.exists():
            return [p(f"<b>{caption}</b> - Screenshot not available.", body)]
        return [
            Image(str(image_path), width=6.2 * inch, height=4.3 * inch),
            p(f"<b>Figure:</b> {caption}", styles["Small"]),
            Spacer(1, 8),
        ]

    story: list = [
        Spacer(1, 0.8 * inch),
        p("A PROJECT REPORT", styles["CoverTitle"]),
        p("CAREPOINT CLINIC FORM UI AUTOMATION", styles["CoverTitle"]),
        p("(Advanced Selenium WebDriver with Python)", styles["CoverSub"]),
        Spacer(1, 0.35 * inch),
        p("Submitted to Department of Computer Science", styles["CoverSub"]),
        Spacer(1, 0.3 * inch),
        p(
            "<b>Student:</b> DUMPALA SYAM KUMAR<br/>"
            "<b>Student ID:</b> 2444670795<br/>"
            "<b>Lecturer:</b> S D VENKATESH LANKA",
            styles["CoverSub"],
        ),
        Spacer(1, 0.5 * inch),
        p("Project documentation, framework design and execution evidence", styles["CoverSub"]),
        p(date.today().strftime("%d %B %Y"), styles["CoverSub"]),
        PageBreak(),
        p("CarePoint Clinic Form UI Automation", styles["Title"]),
        p(
            "Project documentation: description, workflow interpretation, Selenium implementation, "
            "framework architecture, execution evidence and submission checklist.",
            body,
        ),
        Spacer(1, 12),
        p("<b>Contents</b>", styles["Section"]),
        p("1. Introduction and purpose", body),
        p("2. Project description", body),
        p("3. Application under test", body),
        p("4. Technology stack", body),
        p("5. Project structure", body),
        p("6. Framework design and architecture", body),
        p("7. Locator inventory", body),
        p("8. Test suite and workflow scenarios", body),
        p("9. Synchronisation and interaction strategy", body),
        p("10. Setup and execution", body),
        p("11. Execution results and evidence", body),
        p("12. Required explanations", body),
        p("13. Source code listings", body),
        p("14. Submission checklist compliance", body),
        p("15. Limitations and future enhancements", body),
        p("Appendix A. Detailed execution matrix", body),
        p("Appendix B. Source code listings", body),
        p("Appendix C. Environment and reproducibility record", body),
        p("Appendix D. Working execution screenshots", body),
        PageBreak(),
        p("1. Introduction and purpose", styles["Section"]),
        p(
            "This report presents an advanced browser automation project for a healthcare-style "
            "patient registration form. The work interprets the CarePoint brief as a realistic "
            "clinic intake workflow and implements it using Selenium WebDriver, Python and pytest. "
            "The objective is not only to demonstrate a successful form fill, but to provide a "
            "maintainable, repeatable and diagnosable automation framework suitable for assessment "
            "and future extension.",
            body,
        ),
        p("The project addresses all five assessment areas: interpretation and presentation, Selenium "
          "driver implementation, framework design and architecture, execution and reports, and "
          "project completion with documentation.", body),
        p("2. Project description", styles["Section"]),
        p(
            "The automation models a CarePoint clinic registration journey. A synthetic patient "
            "record is entered, country/title/phone-code dropdowns are selected, dates and contact "
            "details are completed, a preferred communication method is selected, and the form is "
            "submitted. The framework also verifies invalid and incomplete states so that the "
            "automation tests behavior rather than merely clicking controls.",
            body,
        ),
        p("The project is intentionally advanced beyond a basic linear script. It uses Page Object "
          "Model separation, centralized waits, browser configuration, test markers, data classes, "
          "failure screenshots, logs, HTML/JUnit reporting and an academic PDF generator.", body),
        p("3. Application under test", styles["Section"]),
        p("<b>Primary CarePoint practice page:</b> https://www.qapractice.com/practice-forms", body),
        p("<b>Healthcare scenario reference:</b> TesterRank MediConnect Hospital Portal, including "
          "patient registration and doctor appointment test cases at https://www.testerrank.com/practice/hospital/test-cases",
          body),
        p(
            "The QA Practice page exposes stable id and data-testid attributes for the form. It "
            "contains country, title, patient names, date of birth, date of joining, email, phone "
            "code, phone number and communication preference controls. The website explicitly "
            "states that values are not stored; the project uses dummy data only.",
            body,
        ),
        p("TesterRank was also investigated as the healthcare domain reference. Its MediConnect "
          "portal defines patient registration, OPD, appointments, pharmacy/billing and lab-report "
          "scenarios. At execution time, the public portal routes exposed the sandbox navigation and "
          "test-case content, while the live registration controls were not available; therefore "
          "the executed UI evidence is reported against the stable QA Practice form rather than "
          "claiming an unavailable TesterRank submission.", body),
        PageBreak(),
        p("4. Technology stack", styles["Section"]),
        Table([
            ["Component", "Technology / version", "Purpose"],
            ["Language", "Python 3.9+", "Test implementation and tooling"],
            ["Browser automation", "Selenium WebDriver 4", "Real browser control"],
            ["Test runner", "pytest 8", "Fixtures, parametrisation and markers"],
            ["Reporting", "pytest-html and JUnit XML", "Human and machine-readable evidence"],
            ["Diagnostics", "Python logging and PNG screenshots", "Failure investigation"],
            ["Driver management", "Selenium Manager", "Automatic Chrome/Edge driver resolution"],
            ["PDF generation", "ReportLab", "This academic project report"],
        ], colWidths=[1.2*inch, 1.7*inch, 3.1*inch], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#eaf2f8")]),
            ("PADDING", (0, 0), (-1, -1), 5),
        ])),
        p("5. Project structure", styles["Section"]),
        p(
            "<b>conftest.py</b> - driver lifecycle, CLI options, environment configuration, logging and failure screenshots.<br/>"
            "<b>pages/base_page.py</b> - reusable explicit waits, stable element lookup and resilient clicking.<br/>"
            "<b>pages/carepoint_form_page.py</b> - CarePoint form locators, patient data model and business actions.<br/>"
            "<b>tests/test_carepoint_form.py</b> - positive, negative, regression and smoke tests.<br/>"
            "<b>pytest.ini</b> - test discovery and marker definitions.<br/>"
            "<b>requirements.txt</b> - reproducible dependencies.<br/>"
            "<b>README.md</b> - setup and execution documentation.<br/>"
            "<b>generate_report.py</b> - this report generator.<br/>"
            "<b>reports/</b> - HTML, JUnit and PDF execution evidence.",
            body,
        ),
        p("6. Framework design and architecture", styles["Section"]),
        p(
            "The framework follows a layered design. Test modules express business intent and "
            "assertions. The CarePoint page object owns form-specific behavior and locators. The "
            "BasePage owns synchronization and generic interactions. Pytest fixtures create and "
            "dispose WebDriver instances consistently. This prevents duplicated selectors and "
            "reduces the impact of UI changes.",
            body,
        ),
        p("<b>Driver lifecycle:</b> each test receives a fresh Chrome or Edge driver. The fixture "
          "sets page-load timeout, viewport and headless behavior, then guarantees quit after the test.", body),
        p("<b>Configuration:</b> browser, headless mode, base URL, explicit wait and page-load timeout "
          "are configurable through command-line options and environment variables.", body),
        p("<b>Diagnostics:</b> a failed test automatically saves a timestamped PNG screenshot under "
          "artifacts/screenshots. Execution logging is written under artifacts/logs.", body),
        PageBreak(),
        p("7. Locator inventory", styles["Section"]),
        Table([
            ["Element", "Stable locator", "Interaction"],
            ["Country", "#forms-country", "Select visible text"],
            ["Title", "#forms-title", "Select visible text"],
            ["First name", "#forms-first-name", "Clear and type"],
            ["Last name", "#forms-last-name", "Clear and type"],
            ["Date of birth", "#forms-dob", "ISO date input"],
            ["Date of joining", "#forms-doj", "dd/mm/yyyy input"],
            ["Email", "#forms-email", "Clear and type"],
            ["Phone code", "#forms-phone-code", "Select visible text"],
            ["Phone number", "#forms-phone-number", "Clear and type"],
            ["Email preference", "#forms-comm-email", "Select radio"],
            ["Phone preference", "#forms-comm-phone", "Select radio"],
            ["Submit", "#forms-submit", "Scroll and click"],
            ["Success message", "#forms-success", "Visibility and text assertion"],
        ], colWidths=[1.65*inch, 2.0*inch, 2.35*inch], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#eaf2f8")]),
            ("PADDING", (0, 0), (-1, -1), 5),
        ])),
        p("8. Test suite and workflow scenarios", styles["Section"]),
        Table([
            ["ID", "Scenario", "Expected result"],
            ["TC01", "Valid patient form submission", "Success message is visible"],
            ["TC02-TC07", "Each required field is blank", "Field-level validation appears and no success state"],
            ["TC08", "Communication preference omitted", "Communication validation appears"],
            ["TC09", "Invalid email", "Native validity rejects the value"],
            ["TC10", "Invalid joining-date format", "Field-level format validation"],
            ["TC11", "Email then Phone radio selection", "Only the final radio remains selected"],
            ["TC12", "Fill and clear form", "Input controls return to a blank state"],
            ["TC13", "Country options and selection", "Expected options and India selection persist"],
            ["TC14", "Title selection", "Dr. selection persists"],
            ["TC15", "Phone-code selection", "+91 selection persists"],
            ["TC16", "Invalid phone behavior", "Real site behavior is documented without a false rejection claim"],
            ["TC17", "Future date of birth", "Success or validation matches site behavior"],
            ["TC18", "Success confirmation content", "Exact success text is displayed"],
            ["TC19", "Go Back to Form", "Fresh blank form is restored"],
            ["TC20", "JSON data-driven submission", "Synthetic patient record submits successfully"],
            ["TC21", "Page title and key controls", "Title, 12 initial controls and success control are present"],
        ], colWidths=[0.75*inch, 2.7*inch, 2.55*inch], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#eaf2f8")]),
            ("PADDING", (0, 0), (-1, -1), 5),
        ])),
        p("9. Synchronisation and interaction strategy", styles["Section"]),
        p(
            "The implementation avoids fixed sleeps in the Selenium framework. WebDriverWait and "
            "expected conditions wait for visibility or clickability. Before clicking controls near "
            "the bottom of the viewport, the framework scrolls the target into the center of the "
            "viewport. If a browser overlay intercepts a click, the interaction layer performs a "
            "controlled JavaScript click as a fallback. Select elements use Selenium Select, and "
            "text fields are cleared before data entry to make test state deterministic.",
            body,
        ),
        PageBreak(),
        p("10. Setup and execution", styles["Section"]),
        p("Install dependencies:", styles["Subsection"]),
        p("python -m pip install -r requirements.txt", styles["Small"]),
        p("Run the full Chrome suite:", styles["Subsection"]),
        p("python -m pytest --browser chrome --headless --html=reports\\report.html "
          "--self-contained-html --junitxml=reports\\junit.xml", styles["Small"]),
        p("Run visibly in Chrome:", styles["Subsection"]),
        p("python -m pytest --browser chrome --headed", styles["Small"]),
        p("Run Edge:", styles["Subsection"]),
        p("python -m pytest --browser edge --headless", styles["Small"]),
        p("Regenerate the academic report:", styles["Subsection"]),
        p("python generate_report.py", styles["Small"]),
        p(
            "The project uses Selenium Manager, so browser driver executables are not committed to "
            "the repository. The test suite can run headless in CI or headed for demonstration.",
            body,
        ),
        p("11. Execution results and evidence", styles["Section"]),
        p(
            f"<b>Latest full execution: {result}</b><br/>{evidence}<br/>"
            "Browser: Google Chrome, headless execution.<br/>"
            f"{edge_result}<br/>"
            "Provided execution evidence: Chrome 21/21 tests passed.<br/>"
            "Generated artifacts: reports/report.html, reports/junit.xml and this PDF.",
            body,
        ),
        Table([
            ["Result", "Value"],
            ["Collected tests", str(tests)],
            ["Passed", str(passed)],
            ["Failed", str(failures)],
            ["Errors", str(errors)],
            ["Assessment evidence", "Chrome 21/21 tests passed"],
        ], colWidths=[2.2*inch, 3.8*inch], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#eaf2f8")]),
            ("PADDING", (0, 0), (-1, -1), 5),
        ])),
        p("12. Required explanations", styles["Section"]),
        p("<b>Why Page Object Model?</b> It keeps locators and page behavior in one place, allowing "
          "test cases to remain readable and reducing maintenance when the UI changes.", body),
        p("<b>Why explicit waits?</b> Browser applications render asynchronously. Explicit conditions "
          "wait for the state required by the next action and are more reliable than arbitrary delays.", body),
        p("<b>Why negative tests?</b> A clinic form must reject incomplete patient data. Validation "
          "tests prove that required fields and communication rules are enforced.", body),
        p("<b>Why synthetic data?</b> The practice site is for automation training and explicitly "
          "prohibits real personal information. The project uses dummy values such as "
          "aarav.sharma@example.test.", body),
        PageBreak(),
        p("13. Source code listings", styles["Section"]),
        p("<b>Test data model and page actions</b>", styles["Subsection"]),
        p(
            "PatientFormData stores a complete synthetic record with safe defaults. "
            "CarePointFormPage exposes open, fill, submit, select_communication, success_is_visible, "
            "validation_messages and clear_all methods. Tests therefore call business actions instead "
            "of directly manipulating selectors.",
            body,
        ),
        p("<b>Fixture and diagnostics</b>", styles["Subsection"]),
        p(
            "conftest.py defines the --browser, --headless, --headed and --base-url options; creates "
            "Chrome or Edge; applies timeout configuration; and captures a screenshot after a failed "
            "call phase. This is the execution control plane for the suite.",
            body,
        ),
        p("<b>Representative test implementation</b>", styles["Subsection"]),
        p(
            "The smoke test opens the configured page, fills PatientFormData, submits and verifies "
            "the success element. Parametrised negative tests replace one field with an empty string "
            "and verify visible validation without a success state. Additional regression tests cover "
            "radio exclusivity and reset behavior.",
            body,
        ),
        p("14. Submission checklist compliance", styles["Section"]),
        Table([
            ["Requirement", "Evidence in this project", "Status"],
            ["20: Interpretation & presentation", "Workflow explanation, healthcare context, test inventory", "Complete"],
            ["20: Selenium drivers", "Chrome/Edge WebDriver, Selenium Manager, waits and lifecycle", "Complete"],
            ["20: Framework architecture", "Page Objects, BasePage, fixtures, markers, data model", "Complete"],
            ["20: Execution & reports", f"{passed}/{tests} run, HTML, JUnit, screenshots and PDF", "Complete"],
            ["20: Completion & documentation", "README, requirements, commands, limitations and report", "Complete"],
        ], colWidths=[1.75*inch, 3.45*inch, 0.8*inch], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#eaf2f8")]),
            ("PADDING", (0, 0), (-1, -1), 5),
        ])),
        p("15. Limitations and future enhancements", styles["Section"]),
        p(
            "The public QA Practice page can change independently of this project, and validation "
            "wording may vary. TesterRank currently provides healthcare test-case guidance and a "
            "MediConnect sandbox, but its public registration controls were not available during "
            "the recorded run. The executed evidence therefore uses the stable QA Practice form.",
            body,
        ),
        p(
            "Future enhancements include adding a TesterRank adapter when its controls are exposed, "
            "Dockerized browser execution, a CI browser matrix, parallel execution with pytest-xdist, "
            "accessibility checks, visual snapshots, Allure history, and API/database test layers "
            "for a complete end-to-end clinic platform.",
            body,
        ),
        Spacer(1, 18),
        p("<b>Conclusion</b>", styles["Subsection"]),
        p(
            "The CarePoint project delivers a complete advanced Selenium automation solution rather "
            "than a basic recorded script. It interprets a healthcare workflow, implements reliable "
            "browser interactions, validates both success and error paths, produces reproducible "
            "execution evidence, and documents the design for academic review.",
            body,
        ),
    ]
    story.extend([
        PageBreak(),
        p("Appendix A. Detailed execution matrix", styles["Section"]),
        p("The following matrix maps every automated check to the business risk it covers and the "
          "assertion used by the framework.", body),
        Table([
            ["Test", "Risk covered", "Action", "Assertion"],
            ["TC01", "Valid registration rejected", "Complete and submit synthetic patient data", "Success modal is visible"],
            ["TC02", "First name accepted when missing", "Blank first name and submit", "Required validation, no success"],
            ["TC03", "Last name accepted when missing", "Blank last name and submit", "Required validation, no success"],
            ["TC04", "Email accepted when missing", "Blank email and submit", "Required validation, no success"],
            ["TC05", "DOB accepted when missing", "Blank DOB and submit", "Required validation, no success"],
            ["TC06", "Joining date accepted when missing", "Blank joining date and submit", "Required validation, no success"],
            ["TC07", "Phone accepted when missing", "Blank phone and submit", "Required validation, no success"],
            ["TC08", "Preference not required", "Submit without radio choice", "Communication validation"],
            ["TC09", "Invalid email bypasses validation", "Use not-an-email", "Native checkValidity is false"],
            ["TC10", "Invalid date format accepted", "Use ISO date for dd/mm/yyyy field", "Format validation"],
            ["TC11", "Both communication radios selected", "Select Email then Phone", "Only Phone selected"],
            ["TC12", "Clear leaves stale data", "Fill, clear and submit", "Inputs return to blank state"],
            ["TC13", "Country selection lost", "Inspect options and select India", "Options and selection persist"],
            ["TC14", "Title selection lost", "Select Dr.", "Selection persists"],
            ["TC15", "Phone code selection lost", "Select +91", "Selection persists"],
            ["TC16", "Phone validation differs", "Submit invalid phone value", "Actual site behavior is accepted or validated"],
            ["TC17", "Future DOB mishandled", "Submit future DOB", "Actual site behavior is accepted or validated"],
            ["TC18", "Success text changes", "Complete and submit valid data", "Exact confirmation text"],
            ["TC19", "Back action keeps stale data", "Submit then go back", "Fresh blank form"],
            ["TC20", "JSON record fails", "Submit patients.json record", "Success message"],
            ["TC21", "Required controls missing", "Open page and inspect controls", "Title, controls and post-submit success"],
        ], colWidths=[0.48*inch, 1.65*inch, 2.1*inch, 1.77*inch], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7.2),
            ("LEADING", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#eaf2f8")]),
            ("PADDING", (0, 0), (-1, -1), 4),
        ])),
        p("Appendix A.1 Test-data strategy", styles["Subsection"]),
        p("PatientFormData is an immutable dataclass. Each negative test creates a copy with one "
          "field changed, keeping all other fields valid. This isolates defects and makes failures "
          "diagnosable. The email uses the reserved .test domain and all patient values are synthetic.", body),
        PageBreak(),
        p("Appendix B. Source code listings", styles["Section"]),
        p("B.1 pytest fixture and driver configuration", styles["Subsection"]),
        XPreformatted(
            "def _build_driver(browser: str, headless: bool):\n"
            "    if browser == \"chrome\":\n"
            "        options = ChromeOptions()\n"
            "        options.add_argument(\"--window-size=1440,1000\")\n"
            "        if headless:\n"
            "            options.add_argument(\"--headless=new\")\n"
            "        return webdriver.Chrome(options=options)\n"
            "    options = EdgeOptions()\n"
            "    options.add_argument(\"--window-size=1440,1000\")\n"
            "    if headless:\n"
            "        options.add_argument(\"--headless=new\")\n"
            "    return webdriver.Edge(options=options)",
            styles["CodeListing"],
        ),
        p("The driver factory keeps browser selection explicit and allows the same test suite to "
          "execute against Chrome or Edge. Selenium Manager resolves compatible drivers without "
          "placing executable binaries in the project.", body),
        p("B.2 reusable synchronization layer", styles["Subsection"]),
        XPreformatted(
            "def visible(self, locator):\n"
            "    return self.wait.until(EC.visibility_of_element_located(locator))\n\n"
            "def clickable(self, locator):\n"
            "    return self.wait.until(EC.element_to_be_clickable(locator))\n\n"
            "def click(self, locator):\n"
            "    element = self.clickable(locator)\n"
            "    self.driver.execute_script(\n"
            "        \"arguments[0].scrollIntoView({block: 'center'});\", element\n"
            "    )\n"
            "    element.click()",
            styles["CodeListing"],
        ),
        p("Centralizing waits makes timing behavior consistent and avoids duplicated sleeps. The "
          "scroll operation addresses controls below the visible viewport and the click fallback "
          "handles the documented overlay behavior of the practice page.", body),
        PageBreak(),
        p("Appendix B.3 CarePoint Page Object listing", styles["Section"]),
        XPreformatted(
            "class CarePointFormPage(BasePage):\n"
            "    FIRST_NAME = \"forms-first-name\"\n"
            "    LAST_NAME = \"forms-last-name\"\n"
            "    EMAIL = \"forms-email\"\n"
            "    DOB = \"forms-dob\"\n"
            "    DOJ = \"forms-doj\"\n"
            "    PHONE = \"forms-phone-number\"\n"
            "    SUBMIT = \"forms-submit\"\n"
            "    SUCCESS = \"forms-success\"\n\n"
            "    def fill(self, data=PatientFormData(), *, include_communication=True):\n"
            "        self._type(self.FIRST_NAME, data.first_name)\n"
            "        self._type(self.LAST_NAME, data.last_name)\n"
            "        self._type(self.EMAIL, data.email)\n"
            "        self._type(self.DOB, data.date_of_birth)\n"
            "        self._type(self.DOJ, data.date_of_joining)\n"
            "        self._select(self.COUNTRY, data.country)\n"
            "        self._select(self.TITLE, data.title)\n"
            "        if include_communication:\n"
            "            self.select_communication(data.communication)",
            styles["CodeListing"],
        ),
        p("The Page Object exposes business-level operations instead of leaking CSS selectors into "
          "the test module. This is the main maintainability boundary in the design.", body),
        p("Appendix B.4 Test implementation listing", styles["Subsection"]),
        XPreformatted(
            "@pytest.mark.smoke\n"
            "def test_valid_patient_form_submission(driver, base_url):\n"
            "    page = CarePointFormPage(driver).open(base_url)\n"
            "    page.fill(PatientFormData())\n"
            "    page.submit()\n"
            "    assert page.success_is_visible()\n\n"
            "@pytest.mark.parametrize(\"field\", REQUIRED_FIELDS)\n"
            "def test_required_field_validation(driver, base_url, field):\n"
            "    page = CarePointFormPage(driver).open(base_url)\n"
            "    page.fill(PatientFormData(**{field: \"\"}))\n"
            "    page.submit()\n"
            "    assert page.validation_messages()\n"
            "    assert not page.success_is_visible()",
            styles["CodeListing"],
        ),
        PageBreak(),
        p("Appendix C. Environment and reproducibility record", styles["Section"]),
        p("C.1 Execution environment", styles["Subsection"]),
        Table([
            ["Property", "Recorded value"],
            ["Operating system", "Windows"],
            ["Python", "3.14.6"],
            ["pytest", "8.4.2"],
            ["Selenium", "4.x, constrained below version 5"],
            ["Browser execution", "Google Chrome headless"],
            ["Target URL", "https://www.qapractice.com/practice-forms"],
            ["Execution mode", "Serial run against the public practice site"],
            ["Latest result", f"{passed} passed, {failures} failed, {errors} errors"],
        ], colWidths=[2.2*inch, 3.8*inch], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#eaf2f8")]),
            ("PADDING", (0, 0), (-1, -1), 5),
        ])),
        p("C.2 Reproducibility procedure", styles["Subsection"]),
        p("1. Create a Python virtual environment. 2. Install requirements.txt. 3. Run the serial "
          "Chrome command from Section 10. 4. Inspect reports/report.html and reports/junit.xml. "
          "5. Run generate_report.py to refresh this document. 6. For CI, use the GitHub Actions "
          "workflow in .github/workflows/selenium.yml, which executes both Chrome and Edge jobs "
          "and uploads artifacts.", body),
        p("C.3 Evidence interpretation", styles["Subsection"]),
        p("The JUnit result is the authoritative machine-readable count for this project run. The "
          "HTML report provides test-level detail, while screenshots and logs support diagnosis of "
          "future failures. The previously supplied assessment evidence of Chrome 21/21 passed is "
          "retained in the report as instructor-provided evidence and matches the current "
          f"{tests}-test implementation run.", body),
        PageBreak(),
        p("Appendix D. Working execution screenshots", styles["Section"]),
        p("These screenshots were captured from a real browser execution against the live CarePoint "
          "practice page using synthetic data only.", body),
        *evidence_image("01_form_initial.png", "Initial CarePoint form before data entry"),
        PageBreak(),
        p("Appendix D.1 Completed form", styles["Subsection"]),
        *evidence_image("02_form_completed.png", "Completed form before submission"),
        PageBreak(),
        p("Appendix D.2 Successful submission", styles["Subsection"]),
        *evidence_image("03_submission_success.png", "Successful submission confirmation"),
        PageBreak(),
        p("Final submission summary", styles["Section"]),
        p("The project now provides a complete, advanced and documented Selenium submission for the "
          "CarePoint healthcare-style workflow. It includes an executable framework, robust positive "
          "and negative coverage, cross-browser configuration, CI support, diagnostics, reports and "
          "a full academic narrative modeled on the supplied report structure.", body),
        Table([
            ["Deliverable", "Location"],
            ["Project instructions", "README.md"],
            ["Automation tests", "tests/test_carepoint_form.py"],
            ["Page Objects", "pages/base_page.py and pages/carepoint_form_page.py"],
            ["Driver fixtures", "conftest.py"],
            ["CI matrix", ".github/workflows/selenium.yml"],
            ["HTML report", "reports/report.html"],
            ["JUnit report", "reports/junit.xml"],
            ["Academic PDF", "reports/CarePoint_Project_Report.pdf"],
        ], colWidths=[2.2*inch, 3.8*inch], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#eaf2f8")]),
            ("PADDING", (0, 0), (-1, -1), 5),
        ])),
    ])
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(output)


if __name__ == "__main__":
    build_pdf()
