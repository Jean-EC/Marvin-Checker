from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as GeckoDriverService
from selenium.common.exceptions import TimeoutException
import os
# This script is supposed to be runned in a cronjob every minutes. You can change the time if you want.
os.environ['DISPLAY'] = ':0'
os.environ['DBUS_SESSION_BUS_ADDRESS'] = 'unix:path=/run/user/1000/bus'
url = "https://my.epitech.eu/"

filename = "website_content.txt"

driver_path = "/usr/bin/geckodriver"

options = Options()
options.add_argument("--headless")
options.profile = "/home/khara/.mozilla/firefox/aqoh1xti.default-release"
service_args = ["--marionette-port", "2828"]
service = GeckoDriverService(executable_path=driver_path, log_path=os.path.devnull, service_args=service_args)
driver = webdriver.Firefox(options=options, service=service)

driver.get(url)

try:
    wait = WebDriverWait(driver, 30)
    login_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mdl-button__ripple-container")))
    print("login_button found!")
except TimeoutException:
    login_button = None
    print("TimeoutException: Login button not found.")

if login_button is not None:
    print("Clicking on login button.")
    login_button.click()

    driver.implicitly_wait(10)

    if url in driver.current_url:
        print("Already logged in.")
    else:
        print("Login successful.")
else:
    print("No login button found. Proceeding to get website content.")

try:
    wait = WebDriverWait(driver, 30)
    main_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))

    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='mdl-card']")))

    content = main_element.get_attribute("innerHTML")
except TimeoutException:
    print("Timed out waiting for main element or content to be present on the page.")
    content = None

if content is not None:
    if os.path.exists(filename):
        with open(filename, "r") as f:
            old_content = f.read()

        if old_content == content:
            print("Website content has not changed.")
            #Uncomment this if you want to get a useless notification every 5 minutes (Obviously only use that to debug uh)
            # os.system("notify-send 'IT DID NOT CHANGE' 'Yea you can go back to sleep'")
        else:
            os.system("notify-send 'IT CHANGED' 'Yea you need to check marvin to see his failed tests'")
            print("Website content has changed.")
            with open(filename, "w") as f:
                f.write(content)
    else:
        print("Website content not found. Creating file.")
        with open(filename, "w") as f:
            f.write(content)
else:
    print("Unable to get website content.")

driver.quit()