import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Set up the directory path where we want to save the HTML file
save_directory = "temp_code/pages"
os.makedirs(save_directory, exist_ok=True)  # Create directory if it doesn't exist

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Start Chrome in maximized mode
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2  # Disable notifications
})

driver = webdriver.Chrome(options=chrome_options)  # Initialize the Chrome driver with options
driver.get("https://useinsider.com/")  # Open the desired page

try:
    # Increase timeout to 20 seconds to allow for slower page loads
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "main")))
    print("Main content loaded successfully.")
except Exception as e:
    print("Failed to load main content:", e)
    # Print out some elements as debug info
    body_elements = driver.find_elements(By.TAG_NAME, "body")
    print(f"Found {len(body_elements)} <body> elements on the page.")

# Save the page source HTML to a file in the specified directory
with open(os.path.join(save_directory, "home_page.html"), "w", encoding="utf-8") as file:
    file.write(driver.page_source)

driver.quit()  # Close the browser
