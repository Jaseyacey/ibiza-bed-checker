from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from sendEmail import call_email_verify_function
import time

def check_date(driver, date_str):
    try:
        # Click on the date input to open the calendar
        date_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'date')))
        date_input.click()

        # Click the right arrow button to move to the next month if needed
        arrow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Move forward to switch to the next month."]'))
        )
        arrow_button.click()

        # Wait for the calendar to update
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'td[aria-label="{date_str}"]'))
        )

        # Find and click the date element
        date_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'td[aria-label="{date_str}"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", date_element)
        driver.execute_script("arguments[0].click();", date_element)

        try:
            date_available = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//span[text()='{date_str}']"))
            )
            if date_available:
                return True
        except TimeoutException:
            return False
    except Exception as e:
        print(f"An error occurred while checking date {date_str}: {e}")
        return False

def perform_actions(dates_to_check):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get('https://www.amanteibiza.com/')

        # Decline cookies
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.scookiebutton.cta.jqdeclinecookies'))).click()

        # Click on the "Reservations" link
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.cbook .cta'))).click()

        for date_str in dates_to_check:
            if check_date(driver, date_str):
                call_email_verify_function(
                    subject=f"Date Found: {date_str}",
                    body=f"The date {date_str} was found on the website.",
                    to_email="jbeedle@gmail.com"
                )
            else:
                print(f"The date {date_str} was not found.")

    finally:
        # Quit the driver
        driver.quit()

def main():
    dates_to_check = [
        "01/10/2024",
        "02/09/2024",
        "03/09/2024",
        "04/09/2024",
        "05/09/2024",
        "06/09/2024",
    ]

    notified_dates = set()

    while True:
        perform_actions(dates_to_check)
        
        notified_dates.update(dates_to_check)

        print("Waiting for 20 minutes...")
        time.sleep(1200)  

if __name__ == "__main__":
    main()


