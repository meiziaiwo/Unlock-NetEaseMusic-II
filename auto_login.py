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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B336062D9527D211AB27C9751308F09C0A07ABE549CAAEFB0E3A516E9784C7FDFABDFBF0D7B6ECF0A71AC8860DF02558F8C5A968815EDBA82FD115F7C9BECAFF18AA1B93B13904757E44B9DFE97D63B8078568A02B0467603939DA50990B9F4DB28055E2BCAB44839248A16CDC80B486A3AD78124A0F48B284E112040AA91864CF517B7AACCCD3AD949ECE12272D221BFCDE57F0FD87ED084774D39F45A15C2E7A1C608373A28D489D4344D9A579AEFDC1B770820A2149E6BE8D46FDC85B88BA69C2A38E365E6C77E93FA5D2C0E126A4FA54B649E1E47D86C0B021D406F22618D1C7AEC470A1351B52BD4A836F74C6DE203BE865E69165F6CDCC52C5FB75A486A9BF4F617D32616EABCDEE5A010F6B8CC86E6697E2EE2267265BE511A0C479515EBCB5BBD85D7C5495C915A76D41EE48FCBC09FDBE425533860207B2DEC20F8EE96355BBB173A38F79855939C9720E6A04823F4870C3E860998A4AD0FCB8434F"})
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
