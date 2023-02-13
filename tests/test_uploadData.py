from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import pytest
import time


def test_scenario1(): #route to match student via navbar
    driver = webdriver.Chrome \
        (service=ChromeService \
            (executable_path=ChromeDriverManager() \
                .install()))
        
    driver.get("http://localhost:5221")
    
    time.sleep(1)

    title = driver.title
    assert title == "Home - My Webpage"

    driver.implicitly_wait(0.5)

    time.sleep(1)
    
    original_window = driver.current_window_handle  
    
    driver.find_element(By.XPATH, \
        "//a[@href='/Upload_Data']").click()
    
    time.sleep(1)

    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break    

    time.sleep(1)

    title = driver.title
    assert title == "Upload Data - My Webpage"
    
    time.sleep(2)

    driver.quit()
