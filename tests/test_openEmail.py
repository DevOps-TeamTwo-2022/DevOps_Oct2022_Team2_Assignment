from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from flaskPy import app

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
        "//a[@href='/Prepare_Email']").click()
    
    time.sleep(1)

    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break    

    time.sleep(1)

    title = driver.title
    assert title == "Prepare Email - My Webpage"
    
    time.sleep(2)

    driver.find_element(By.CLASS_NAME,"button").click()   

    time.sleep(2)    

    response = app.test_client().get('/Prepare_Email')
  
    email_Open = app.test_client().get('/SendFile')
  
    tempList = [str(response),str(email_Open)]
  
    print("Redirect to main",tempList[0],"Open Prepare_Email.html",tempList[1])
  
    errors = []

    if "500 internal" in tempList[0]:
        errors.append("Warning! 500 internal server error!")   
    if not "302 FOUND" in tempList[0]:
        errors.append("Warning! Redirection not found!")
    if "405 NOT FOUND" in tempList[1]:
        errors.append("Warning! 405 Not Found for Match_Student.html!")     

    assert not errors, "errors occured:\n{}".format("\n".join(errors))  

    driver.quit()