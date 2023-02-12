from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains

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

    driver.implicitly_wait(1)

    time.sleep(1)
    
    original_window = driver.current_window_handle  
    
    driver.find_element(By.XPATH, \
        "//a[@href='/Match_Student']").click()
    
    time.sleep(1)

    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break    

    time.sleep(1)

    title = driver.title
    assert title == "Match Students - My Webpage"
    
    time.sleep(2)

    nav_button = driver.find_element(by=By.ID, value="companySelected")
    
    nav_button.click()
    time.sleep(2)
       
    CompanyList = driver.find_element(by=By.ID, value="companySelected")
    CompanyList.send_keys("Company A,Software Developer")
    CompanyList.click()
    time.sleep(4)

    Status = driver.find_element(by=By.ID, value="assignmentSelected")
    Status.send_keys("Pending confirmation")
    Status.click()
    time.sleep(4)
    
    driver.find_element(By.CLASS_NAME,"btn").click()       
    time.sleep(5)    
    
  
    driver.quit()
