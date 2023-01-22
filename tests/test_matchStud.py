from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

import time

def test_scenario1(): #route to match student via navbar

    service = ChromeService(executable_path=ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service)

    driver.get("http://localhost:5221")
    
    time.sleep(1)

    title = driver.title
    assert title == "Home - My Webpage"

    driver.implicitly_wait(0.5)

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
    
    time.sleep(3)

    driver.quit()

def test_scenario2(): #if no changes made in table, upon submitting/POST must display 0 changes made
    driver = webdriver.Chrome \
        (service=ChromeService \
            (executable_path=ChromeDriverManager() \
                .install()))

    driver.get("http://localhost:5221/Match_Student")
    
    time.sleep(1)
    
    title = driver.title
    assert title == "Match Students - My Webpage"
    
    time.sleep(1)
    
    driver.find_element(By.CLASS_NAME,"btn").click()
    
    time.sleep(1)
    
    sessionVar_Result = driver.find_element(By.CLASS_NAME,"sessionVars")
    
    time.sleep(1)
    
    sesVar_Value = sessionVar_Result.text
    
    time.sleep(1)
    
    assert sesVar_Value == "0 tables updated"
    
    time.sleep(3)

    driver.quit()    
    
def test_scenario3(): #if companyList has selection, table updates
    driver = webdriver.Chrome \
        (service=ChromeService \
            (executable_path=ChromeDriverManager() \
                .install()))

    driver.get("http://localhost:5221/Match_Student")
    
    time.sleep(1)
    
    title = driver.title
    assert title == "Match Students - My Webpage"
    
    time.sleep(1)      
        