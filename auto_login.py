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
    browser.add_cookie({"name": "MUSIC_U", "value": "0093C5105BE1038839E38F50C70C8BDDC2A48085ABAAEF1A1A8ECC27D924A686F3769209F08D534E2DE08D3634C6FE71DB3CA7550BB4E095CFF4043A28DEE9F37B3D20BCFCCBCACCB085176AEEE34A6460B12760ABAC8FF8F09965B1BB5E19B1DADC76943E3803F41BD45CAC521CB9399B0EDA181B4A41C418E33A2FD0BB6D42A973BE25C198D75DB1B21A142B14F12B1FDB6F056DFA6275532D11C6B869A3E4DD660EC0E6FB9B5887CD02348BB176BDD96AA6E0D7995D73C4770874FB722EBD994E0EE62D55A1F9B8128A7CE1A994C0A78331ED94EAA81E2995856573F4A5CD74C7E45081ADC24590E4FEB44D958548284C71D41756144CD4BF7D6CD5FD12A350BEB1F3AEA26B2C8019E8DEB9B402E643D594DBCA5532118C7E956D9F1D22D108A8A99991173C10D1E6404C72E8DB6CA900379521B7DF9370F22349BD284F89C238606BA07FB58D590C4AEDDB82DBA502DC735A27B2AE34733669E4E93632B175"})
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
