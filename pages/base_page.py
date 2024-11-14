import os
import time
from datetime import datetime
import allure
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        """
        Initialize the BasePage with the provided driver instance and create a directory for screenshots.
        """
        self.driver = driver
        self.screenshot_dir = "Screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def wait_for_element(self, locator, timeout=10):
        """
        Waits for an element to become visible within the specified timeout.

        :param locator: Locator for the target element.
        :param timeout: Maximum wait time (in seconds).
        :return: Web element if found within the timeout.
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            allure.attach(f"Element with locator {locator} was not found within {timeout} seconds.",
                          name="Wait for Element Timeout", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Scrolling element into view and taking centered screenshot")
    def take_centered_screenshot(self, name, locator, browser_name=None):
        """
        Scrolls the element into view (aligned with the top of the viewport) and takes a screenshot.

        :param name: Name for the screenshot file.
        :param locator: Locator of the element to scroll into view.
        :param browser_name: Optional, name of the browser to store screenshots separately by browser.
        :return: File path of the saved screenshot.
        """
        try:
            # Locate and scroll element into view
            element = self.wait_for_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'start'});", element)
            time.sleep(1)  # Brief pause for element to settle

            # Take the screenshot
            return self.take_screenshot(name, browser_name)
        except TimeoutException:
            allure.attach(f"Element for screenshot not found: {locator}", name="Screenshot Error",
                          attachment_type=allure.attachment_type.TEXT)
            raise

    def take_screenshot(self, name, browser_name=None):
        """
        Captures a screenshot with a timestamped filename, saved in a browser-specific subdirectory.

        :param name: Name for the screenshot file.
        :param browser_name: Optional, name of the browser to organize screenshots.
        :return: File path of the saved screenshot.
        """
        # Use 'default' if browser name isn't provided
        if not browser_name:
            browser_name = self.driver.capabilities.get('browserName', 'default')

        # Create a subdirectory for the specified browser
        browser_dir = os.path.join(self.screenshot_dir, browser_name)
        os.makedirs(browser_dir, exist_ok=True)

        # Generate a unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(browser_dir, f"{name}_{timestamp}.png")

        # Save and attach screenshot to Allure report
        if self.driver.save_screenshot(filename):
            allure.attach.file(filename, name=f"Screenshot: {name}", attachment_type=allure.attachment_type.PNG)
            return filename
        return None

    @allure.step("Select option '{option_text}' from dropdown")
    def select_dropdown_option(self, dropdown_locator, option_text, option_timeout=15):
        """
        Select an option from a dropdown by visible text, with a fixed delay to ensure elements are loaded.

        :param dropdown_locator: Locator for the dropdown element.
        :param option_text: Text of the option to select from the dropdown.
        :param option_timeout: Maximum time to wait for the options to appear.
        """
        try:
            # Step 1: Wait for 10 seconds to ensure dropdown options are fully loaded
            time.sleep(10)

            # Step 2: Click on the dropdown after ensuring options are loaded
            dropdown = self.wait_for_element(dropdown_locator, timeout=option_timeout)
            dropdown.click()

            # Step 3: Locate and click the desired option
            option_locator = (By.XPATH, f"//li[contains(@class, 'select2-results__option') and text()='{option_text}']")
            option = self.wait_for_element(option_locator, timeout=option_timeout)
            option.click()

            allure.attach(f"Selected option: {option_text}", name="Dropdown Option Selection",
                          attachment_type=allure.attachment_type.TEXT)
        except TimeoutException:
            # Capture error details with a screenshot and Allure message if option selection fails
            error_message = f"Option '{option_text}' not found in dropdown after waiting {option_timeout} seconds."
            self.take_screenshot("dropdown_option_not_found")
            allure.attach(error_message, name="Dropdown Option Selection Error",
                          attachment_type=allure.attachment_type.TEXT)
            raise
