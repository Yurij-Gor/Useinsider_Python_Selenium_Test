# Useinsider Python Selenium Test Project

## Description
This project is designed for automated UI testing of the Insider Careers page. The tests are written in Python using the `pytest` framework with `Selenium` for browser automation and `Allure` for test reporting. The project allows for testing in both Chrome and Firefox browsers, with reports generated locally.

The primary objective is to validate key functionalities on the Insider Careers page, including navigation, verification of block elements, filter application, and job listing actions.

## Test Results
View the Allure Test Report:  
[Allure Report](https://yurij-gor.github.io/Useinsider_Python_Selenium_Test/)

## Technologies
This project utilizes the following technologies:

- **Python 3.x**: The programming language for writing tests.
- **Selenium**: A browser automation tool for performing UI actions.
- **Pytest**: A framework for writing and executing tests.
- **Allure**: A reporting tool for generating detailed test reports.

## Installation
Clone the repository and install the dependencies:

```bash
git clone https://github.com/Yurij-Gor/Useinsider_Python_Selenium_Test.git
cd Useinsider_Python_Selenium_Test
pip install -r requirements.txt
```

## Running Tests

To run the tests in Chrome and generate a report, execute the following command:

```bash
pytest -k "chrome" --alluredir=allure-results
```

To run the tests in Firefox and generate a report, use:

```bash
pytest -k "firefox" --alluredir=allure-results
```

To run the tests in Chrome and Firefox, and generate a report, use:

```bash
pytest --alluredir=allure-results
```

After running the tests, generate a report with the following command:

```bash
allure serve allure-results
```

This command will start a local server and open the Allure report in your default web browser.

## Project Structure

The project has the following structure:

```
Useinsider_Python_Selenium_Test/
├── allure-results/            # Directory for Allure report files
├── drivers/                   # WebDriver executables for Chrome and Firefox
│   ├── chromedriver.exe
│   └── geckodriver.exe
├── pages/                     # Page Object Model files for different pages
│   ├── __init__.py
│   ├── base_page.py           # Base class for all page objects
│   ├── careers_page.py        # Page object for Careers page
│   ├── home_page.py           # Page object for Home page
│   ├── open_positions_page.py # Page object for Open Positions page
│   └── quality_assurance_page.py # Page object for Quality Assurance page
├── Screenshots/               # Directory for screenshots (organized by browser)
│   ├── chrome/
│   └── firefox/
├── tests/                     # Directory with test files
│   ├── __init__.py
│   └── test_insider.py        # Main test file for Insider Careers page
├── .gitignore                 # Files and folders ignored by Git
├── pytest.ini                 # Pytest configuration file with custom markers
├── README.md                  # Project documentation file
└── requirements.txt           # Project dependencies
```

