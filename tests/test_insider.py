import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.quality_assurance_page import QualityAssurancePage
from pages.open_positions_page import OpenPositionsPage


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    """Initialize the browser driver based on the parameter (Chrome or Firefox)."""
    if request.param == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=chrome_options)
    elif request.param == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.set_preference("dom.webnotifications.enabled", False)
        driver = webdriver.Firefox(options=firefox_options)
    else:
        raise ValueError(f"Unsupported browser: {request.param}")

    driver.maximize_window()
    yield driver
    driver.quit()


@allure.feature("Insider Careers Testing - Careers Page Validation")
@allure.story("Navigate, verify blocks, apply filters, and confirm job listings")
@allure.title("Test navigation and verification on Insider Careers page")
@allure.description("""
Test case to verify key steps on the Insider website:
1. Navigate to the Careers page and open Careers section.
2. Verify the presence of key blocks with expected names on the Careers page.
3. Navigate to the QA job listings page.
4. Apply location and department filters on the QA jobs listing.
5. Confirm navigation to the Lever application form after clicking 'View Role' on a job listing.
""")
@pytest.mark.usefixtures("driver")
def test_insider_careers(driver):
    errors = []  # List to collect errors without halting the test

    # Step 1: Navigate to the Careers page
    home_page = HomePage(driver)
    with allure.step("Step 1: Navigate to Careers page and open Careers section"):
        try:
            home_page.open()
            home_page.go_to_careers()
        except (TimeoutException, NoSuchElementException) as e:
            error_message = f"Failed to navigate to Careers page: {str(e)}"
            allure.attach(error_message, name="Navigation Error", attachment_type=allure.attachment_type.TEXT)
            errors.append(error_message)

    # Step 2: Verify presence of key blocks on the Careers page
    careers_page = CareersPage(driver)
    with allure.step("Step 2: Verify presence of key blocks on the Careers page"):
        for block_name in ["teams", "locations", "life_at_insider"]:
            try:
                careers_page.verify_block_presence(block_name)
            except AssertionError as e:
                screenshot_path = careers_page.take_screenshot(f"{block_name}_verification_failure")
                if screenshot_path:
                    allure.attach.file(screenshot_path, name=f"{block_name.capitalize()} Verification Failure Screenshot", attachment_type=allure.attachment_type.PNG)
                errors.append(f"{block_name.capitalize()} verification error: {str(e)}")

    # Step 3: Navigate to QA page
    qa_page = QualityAssurancePage(driver)
    with allure.step("Step 3: Navigate to QA job listings"):
        try:
            qa_page.open()
            qa_page.click_see_all_qa_jobs()
        except (TimeoutException, NoSuchElementException) as e:
            screenshot_path = qa_page.take_screenshot("qa_jobs_navigation_failure")
            if screenshot_path:
                allure.attach.file(screenshot_path, name="QA Jobs Navigation Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            errors.append(f"QA Jobs navigation error: {str(e)}")

    # Step 4: Apply filters and verify job listings
    open_positions_page = OpenPositionsPage(driver)
    with allure.step("Step 4: Apply filters and verify QA jobs listing"):
        try:
            open_positions_page.apply_filters()
            open_positions_page.verify_jobs()
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            screenshot_path = open_positions_page.take_screenshot("job_filters_verification_failure")
            if screenshot_path:
                allure.attach.file(screenshot_path, name="Job Filters Verification Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            errors.append(f"Job Filters verification error: {str(e)}")

    # Step 5: Click "View Role" and verify navigation to Lever application form page
    with allure.step("Step 5: Click 'View Role' and verify navigation to Lever application form page"):
        try:
            open_positions_page.open_first_job()
        except Exception as e:
            error_message = f"Lever application navigation error: {str(e)}"
            allure.attach(error_message, name="Lever Navigation Error", attachment_type=allure.attachment_type.TEXT)
            errors.append(error_message)

    # Final assertion to mark test as failed if any errors were collected
    if errors:
        allure.attach("\n".join(errors), name="Collected Errors", attachment_type=allure.attachment_type.TEXT)
        assert False, "Test failed with errors: " + "; ".join(errors)
