from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class QualityAssurancePage(BasePage):
    URL = "https://useinsider.com/careers/quality-assurance/"
    SEE_ALL_QA_JOBS_LOCATOR = (By.CSS_SELECTOR, ".btn-outline-secondary")

    def open(self):
        self.driver.get(self.URL)

    def click_see_all_qa_jobs(self):
        """Click the 'See all QA jobs' button and wait for the page to load."""
        self.wait_for_element(self.SEE_ALL_QA_JOBS_LOCATOR).click()
