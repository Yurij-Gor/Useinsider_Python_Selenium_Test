from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import time
import allure


# HomePage class representing actions on the Insider home page
class HomePage(BasePage):
    URL = "https://useinsider.com/"  # URL for the Insider home page
    COMPANY_MENU_LOCATOR = (By.XPATH, "//nav//a[contains(text(), 'Company')]")  # Locator for 'Company' menu
    CAREERS_LINK_LOCATOR = (By.XPATH, "//a[text()='Careers']")  # Locator for 'Careers' link

    # Locators for the cookie acceptance banner
    COOKIE_BANNER_LOCATOR = (By.CSS_SELECTOR, "#cookie-law-info-bar")
    ACCEPT_COOKIES_BUTTON_LOCATOR = (By.CSS_SELECTOR, "#wt-cli-accept-all-btn")

    def open(self):
        """Open the Insider home page and accept cookies if prompted."""
        self.driver.get(self.URL)
        self.accept_cookies()  # Accept cookies after opening the page

    @allure.step("Accept cookies on the website if the banner is present")
    def accept_cookies(self):
        """Click on the Accept Cookies button if the cookie banner is displayed."""
        try:
            # Check if the cookie banner is displayed and click the accept button
            cookie_banner = self.wait_for_element(self.COOKIE_BANNER_LOCATOR, timeout=5)
            if cookie_banner:
                accept_button = self.wait_for_element(self.ACCEPT_COOKIES_BUTTON_LOCATOR)
                accept_button.click()
                allure.attach("Accepted cookies.", name="Cookie Acceptance")
                time.sleep(1)  # Brief wait to ensure the banner is dismissed
        except TimeoutException:
            allure.attach("No cookie banner found; proceeding without interaction.", name="Cookie Banner Status")

    def go_to_careers(self):
        """Navigate to the Careers page through the Company menu."""
        # Wait for and click the 'Company' menu
        company_menu = self.wait_for_element(self.COMPANY_MENU_LOCATOR)
        company_menu.click()

        # Wait for and click the 'Careers' link
        careers_link = self.wait_for_element(self.CAREERS_LINK_LOCATOR)
        careers_link.click()
