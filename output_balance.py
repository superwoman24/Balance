import json
import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Load credentials from .env file
load_dotenv()
card_number = os.getenv("CARD_NUMBER")
password = os.getenv("PASSWORD")

# WebDriver setup
driver = webdriver.Chrome(options=Options())
driver.get('https://allengroups.net/online-recharge/')

# Login
driver.find_element(By.NAME, 'cardno').send_keys(card_number)
driver.find_element(By.NAME, 'password').send_keys(password)
driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

# Wait and get balance
try:
    wait = WebDriverWait(driver, 20)
    balance_label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(),"
                                                                         "'Smart Card Balance')]")))

    if balance_label.is_displayed():
        balance_text = balance_label.text.strip()
        balance = balance_text.split('₹ ')[1] if '₹' in balance_text else None

        if balance is not None:
            print(f"Your balance amount is ₹ {balance}.")
        else:
            print('Failed to retrieve balance.')
    else:
        print('Balance label is not visible.')

except TimeoutException:
    print("Timed out waiting for balance element to load.")
except NoSuchElementException:
    print("Balance label element not found.")

driver.quit()
