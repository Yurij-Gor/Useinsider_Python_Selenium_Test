import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage


class CareersPage(BasePage):
    URL = "https://useinsider.com/careers/"

    EXPECTED_BLOCKS = {
        "teams": {
            "locator": (By.CSS_SELECTOR, "#career-find-our-calling"),
            "expected_name": "Teams",
            "header_tag": "h3"
        },
        "locations": {
            "locator": (By.CSS_SELECTOR, "#career-our-location"),
            "expected_name": "Locations",
            "header_tag": "h3"
        },
        "life_at_insider": {
            "locator": (By.CSS_SELECTOR, "section.elementor-section:nth-child(6)"),
            "expected_name": "Life at Insider",
            "header_tag": "h2"
        },
    }

    def open(self):
        """Open the Careers page directly and wait until it is fully loaded."""
        self.driver.get(self.URL)
        self.wait_for_element((By.TAG_NAME, "body"))  # Ensure page is fully loaded

    @allure.step("Verify presence and expected name of block: {block_name}")
    def verify_block_presence(self, block_name):
        """
        Verify the presence of a specific block and its expected name.
        """
        block_data = self.EXPECTED_BLOCKS.get(block_name)
        if not block_data:
            raise ValueError(f"No configuration found for block: {block_name}")

        result = self._verify_block(block_data["locator"], block_data["expected_name"], block_data["header_tag"])

        if result["name_mismatch"]:
            self.take_centered_screenshot(f"{block_name}_name_mismatch", block_data["locator"])
            allure.attach(
                f"Expected: '{result['expected_name']}', Found: '{result['actual_name']}'",
                name=f"{block_name.capitalize()} Verification Result", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError(
                f"Name mismatch for block '{block_name}': Expected '{result['expected_name']}', but found '{result['actual_name']}'")

    def _verify_block(self, locator, expected_name, header_tag):
        """Locate block, scroll if necessary, and verify title."""
        try:
            block = self.wait_for_element(locator, timeout=3)
            actual_name = self._get_block_title(block, header_tag)
            return {
                "found": True,
                "name_mismatch": actual_name != expected_name,
                "actual_name": actual_name,
                "expected_name": expected_name
            }
        except (TimeoutException, NoSuchElementException):
            return self._scroll_and_verify_block(locator, expected_name, header_tag)

    @staticmethod
    def _get_block_title(block, header_tag):
        """Retrieve the block title using the specified header tag."""
        try:
            return block.find_element(By.TAG_NAME, header_tag).text.strip()
        except NoSuchElementException:
            raise NoSuchElementException(f"No title element found in block using tag '{header_tag}'")

    def _scroll_and_verify_block(self, locator, expected_name, header_tag):
        """Scroll down until the block is located, and verify the title if found."""
        max_scroll_attempts = 6
        scroll_height = 1000
        block = None

        for _ in range(max_scroll_attempts):
            try:
                block = self.wait_for_element(locator, timeout=5)
                self.take_centered_screenshot("scrolling_to_block", locator)
                break
            except TimeoutException:
                self.driver.execute_script(f"window.scrollBy(0, {scroll_height});")

        actual_name = self._get_block_title(block, header_tag) if block else ""
        return {
            "found": bool(block),
            "name_mismatch": actual_name != expected_name,
            "actual_name": actual_name,
            "expected_name": expected_name
        }
