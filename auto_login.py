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
    browser.add_cookie({"name": "MUSIC_U", "value": "000B035ACA60EDF265F5ACE598E7F950DF0F1C27B9DFFDF24AE7404807BBB3EC7712D1240EE7143E00CFDAFE5D8EC02B880311FCA206891AFCAD8EB6C4CD3D0CA4A7DA832C79EDCC3B2E003D1928008E286349576F8F1DDB912246E53B3850EE6D04EAD18DD3DD56AB80922099A64982F1DBD7702066D4830076EC2D6E8A9295A8AC0D688C04C5BAEEBD1549B464AD7513D54DC10D7C0D5DDC253EC53BD384DAE181604F931AC9D6680CB7FE356936A2EA4A5CBFCFA77D82EEBDBB4258C18AF378BE990AADCDE9120B1F18AC0BB999BDBAB214E1375B331498272673A32FA6414E6DEFA26DCCEAC8BCC529E2B8437559ED14EF829829FB53F7EEA2285C6999E5BE110D5F127E0A77CB1A48B0FD76B38D8C961581F8539B1EAFAEC0BABFCA639090324B4731F607FFD6997D5BF1A4C7BD9DD3D869130DB3F9E12C76CB2CC0B4743C25AD52ED71DA3C34C89732E0AD2E89F9D0D5D47761DDFE185F2CE415C9BE007C"})
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
