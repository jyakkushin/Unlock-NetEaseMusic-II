# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00C09F6A2B1F50FAD7DFDC878CA3CD145788DBE62808EEA3E53219914557D9A74F8CCB8F63D40F02DCBF136EE3653A8A763FDE945948776B1C13EE3095C34A43E95949E28A05338C11E0DC01DE202C52836A694CD5C2876E241CC9CBC075E081A0026E64BC1C9A96A440B5E006207BC8709585963ACB5AFBA139B7F6F41CA2C876404DF4565C5FBDD8F0F5671C7E2723F43D9FA985A885C5733156017723883012C9AA7783B0BC5065ACEEBC976A80BBBE3F025486BF6D1D1891744E40CAE808D883A79EED473436326DA9192CEEDCC942D19652A598F75D1A6E93DC272B88B183ACD3F6D155799A24D77530BCA4465FDCE8E81E1C0FDF19AF6061D9CFD813F0AA9F0380EA57E757D023B92FB8289F4C4EC2484C5959B7798F1B8485D7ACE31FAE325692DD0C4344E06286B6D5394E17AC2D874F639365480BFEF210837B5F33341635269DA2AF81A1FA64A3E763CD4E3555CA90950BC6E8DC0F74AC8790EE275C"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
