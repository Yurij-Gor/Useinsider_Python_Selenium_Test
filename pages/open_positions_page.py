import time
import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage


class OpenPositionsPage(BasePage):
    # Locators for filter dropdowns
    LOCATION_FILTER_LOCATOR = (By.CSS_SELECTOR, "#select2-filter-by-location-container")
    DEPARTMENT_FILTER_LOCATOR = (By.CSS_SELECTOR, "#select2-filter-by-department-container")

    # Locators for job listing elements
    JOB_LIST_LOCATOR = (By.CSS_SELECTOR, "#jobs-list")  # Main container for the job listings
    JOB_ITEM_LOCATOR = (By.CSS_SELECTOR, ".position-list-item")  # Locator for each job item
    POSITION_NAME_LOCATOR = (By.CSS_SELECTOR, ".position-title")  # Position title within each job item
    DEPARTMENT_LOCATOR = (By.CSS_SELECTOR, ".position-department")  # Department within each job item
    LOCATION_LOCATOR = (By.CSS_SELECTOR, ".position-location")  # Location within each job item
    VIEW_ROLE_BUTTON_LOCATOR = (By.CSS_SELECTOR, "a.btn:nth-child(4)")  # Alternative locator for "View Role" button

    @allure.step("Apply filters for Istanbul, Turkey and Quality Assurance")
    def apply_filters(self):
        """
        Apply location and department filters on the job listing page.
        """
        try:
            # Select 'Istanbul, Turkey' in the location filter
            self.select_dropdown_option(
                self.LOCATION_FILTER_LOCATOR,
                "Istanbul, Turkey"
            )

            # Select 'Quality Assurance' in the department filter
            self.select_dropdown_option(
                self.DEPARTMENT_FILTER_LOCATOR,
                "Quality Assurance"
            )

            # Short delay to ensure filters are applied
            time.sleep(2)

            # Attach confirmation message for applied filters
            allure.attach("Filters applied: Istanbul, Turkey; Quality Assurance", name="Filter Details")
        except Exception as e:
            # Capture error details and screenshot in case of failure
            self.take_screenshot("apply_filters_failure")
            allure.attach(str(e), name="Filter Application Error", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Check that job listings are displayed and match filter criteria")
    def verify_jobs(self):
        """Verify that job listings match the selected filters."""
        try:
            self.driver.execute_script("window.scrollTo(0, 500);")  # Scroll down to reveal job listings
            job_list_container = self.wait_for_element(self.JOB_LIST_LOCATOR)
            jobs = job_list_container.find_elements(*self.JOB_ITEM_LOCATOR)
            assert jobs, "No jobs were found after applying filters"
            allure.attach(f"Found {len(jobs)} job listings after applying filters.", name="Job Listing Count")

            for job in jobs:
                position_name = job.find_element(*self.POSITION_NAME_LOCATOR).text
                department_name = job.find_element(*self.DEPARTMENT_LOCATOR).text
                location_name = job.find_element(*self.LOCATION_LOCATOR).text

                allure.attach(f"Position: {position_name}", name="Position Verification")
                allure.attach(f"Department: {department_name}", name="Department Verification")
                allure.attach(f"Location: {location_name}", name="Location Verification")

                assert "Quality Assurance" in position_name, f"Unexpected position name: {position_name}"
                assert "Quality Assurance" in department_name, f"Unexpected department: {department_name}"
                assert "Istanbul, Turkey" in location_name, f"Unexpected location: {location_name}"
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            # Attach the exception message to Allure and re-raise the exception
            allure.attach(f"Error encountered during job listing verification: {str(e)}",
                          name="Job Verification Error", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Open the first job listing and verify redirection to Lever application form")
    def open_first_job(self):
        """Open the first job listing by hovering over the title and clicking the 'View Role' button, then verify redirection."""
        expected_url_substring = "https://jobs.lever.co/useinsider/"

        try:
            with allure.step("Hover over the job title to reveal 'View Role' button"):
                # Hover over the title of the first job item to reveal the button
                first_job_title = self.wait_for_element(self.POSITION_NAME_LOCATOR)
                ActionChains(self.driver).move_to_element(first_job_title).perform()  # Move cursor to job title

                # After hovering, attempt to find and click the 'View Role' button
                view_role_button = self.wait_for_element(self.VIEW_ROLE_BUTTON_LOCATOR, timeout=10)
                initial_tab_count = len(self.driver.window_handles)  # Count tabs before clicking
                view_role_button.click()
                allure.attach("Clicked 'View Role' button.", name="Click Info",
                              attachment_type=allure.attachment_type.TEXT)

                # Wait for a new tab to open
                WebDriverWait(self.driver, 10).until(
                    lambda d: len(d.window_handles) > initial_tab_count,
                    message="New tab did not open after clicking 'View Role' button."
                )

                # Switch to the new tab
                self.driver.switch_to.window(self.driver.window_handles[-1])
                allure.attach("Switched to new tab successfully.", name="Tab Switch Info",
                              attachment_type=allure.attachment_type.TEXT)

            # Step to wait for the page to load
            with allure.step("Wait for page to load in new tab"):
                time.sleep(5)  # Simple wait to ensure page has loaded
                allure.attach("Waited 5 seconds for the page to load.", name="Wait Info",
                              attachment_type=allure.attachment_type.TEXT)

            # Step to check the URL
            with allure.step("Verify URL in the new tab"):
                current_url = self.driver.current_url
                allure.attach(f"Expected URL to contain: {expected_url_substring}", name="Expected URL",
                              attachment_type=allure.attachment_type.TEXT)
                allure.attach(f"Actual URL: {current_url}", name="Actual URL",
                              attachment_type=allure.attachment_type.TEXT)
                assert expected_url_substring in current_url, (
                    f"Expected URL to contain '{expected_url_substring}', but found: {current_url}"
                )

        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            # Capture URL in case of failure and attach to Allure report
            current_url = self.driver.current_url if len(
                self.driver.window_handles) > initial_tab_count else "Tab did not open"
            error_message = f"Expected Lever URL to contain '{expected_url_substring}', but current URL is: {current_url}"
            allure.attach(error_message, name="Lever Application Navigation Error",
                          attachment_type=allure.attachment_type.TEXT)
            raise e
