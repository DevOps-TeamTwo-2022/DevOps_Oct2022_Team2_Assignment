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

    driver.quit()


def test_scenario2(): #if no changes made in table, upon submitting/POST must display 0 changes made
    
    driver=recursiveMatchStud()
    
    driver.find_element(By.CLASS_NAME,"btn").click()
    
    time.sleep(1)
    
    sessionVar_Result = driver.find_element(By.CLASS_NAME,"sessionVars")
    
    time.sleep(1)
    
    sesVar_Value = sessionVar_Result.text
    
    time.sleep(1)
    
    assert sesVar_Value == "0 tables updated"
    
    time.sleep(2)

    driver.quit()    

  
def test_scenario3(): #if companyList has selection, table updates
    
    driver=recursiveMatchStud()
    
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, '[id=\\"username\\"]')))
    
    select = Select(driver.find_element(By.ID,'companySelected'))   

    theOptions = select.options    
    
    assert theOptions[0].get_attribute("value") == "Unassigned"
    
    time.sleep(2)
    
    select.options[1].click()       
    
    time.sleep(2)
    
    driver.find_element(By.CLASS_NAME,"btn").click()
    
    time.sleep(1)
    
    sessionVar_Result = driver.find_element(By.CLASS_NAME,"sessionVars")
    
    time.sleep(1)
    
    sesVar_Value = sessionVar_Result.text
    
    time.sleep(1)
    
    select = Select(driver.find_element(By.ID,'companySelected'))
    
    theOptions = select.options  
    
    assert sesVar_Value != "0 tables updated"
    assert theOptions[0].get_attribute("value") != "Unassigned"
     
    time.sleep(2)

    driver.quit()
 
    
def test_scenario4(): #if companyList has selection, unassign the selection,table updates
    
    driver=recursiveMatchStud()
    
    select = Select(driver.find_element(By.ID,'companySelected'))   
 
    theOptions = select.options    
    
    assert theOptions[0].get_attribute("value") != "Unassigned"
    
    time.sleep(2)
    
    select.options[1].click()       
    
    time.sleep(2)
    
    driver.find_element(By.CLASS_NAME,"btn").click()
    
    time.sleep(1)
    
    sessionVar_Result = driver.find_element(By.CLASS_NAME,"sessionVars")
    
    time.sleep(1)
    
    sesVar_Value = sessionVar_Result.text
    
    time.sleep(1)
    
    select = Select(driver.find_element(By.ID,'companySelected'))
    
    theOptions = select.options  
    
    assert sesVar_Value != "0 tables updated"
    assert theOptions[0].get_attribute("value") == "Unassigned"
    
    time.sleep(2)

    driver.quit()                     

def test_scenario5(): #if status has selection, table doesnt update
    
    driver=recursiveMatchStud()
    
    select = Select(driver.find_element(By.ID,'assignmentSelected'))   

    theOptions = select.options    
    
    assert theOptions[0].get_attribute("value") == "Unassigned"
    
    time.sleep(2)
    
    select.options[1].click()       
    
    time.sleep(2)
    
    driver.find_element(By.CLASS_NAME,"btn").click()
    
    time.sleep(1)
    
    sessionVar_Result = driver.find_element(By.CLASS_NAME,"sessionVars")
    
    time.sleep(1)
    
    sesVar_Value = sessionVar_Result.text
    
    time.sleep(1)
    
    select = Select(driver.find_element(By.ID,'assignmentSelected'))
    
    theOptions = select.options  
    
    assert sesVar_Value == "0 tables updated"
    assert theOptions[0].get_attribute("value") == "Unassigned"
     
    time.sleep(2)

    driver.quit()

def test_scenario6(): #if companyList has selection, change status to confirmed
    
    driver=recursiveMatchStud()
    
    select = Select(driver.find_element(By.ID,'companySelected'))   

    theOptions = select.options    
    
    assert theOptions[0].get_attribute("value") == "Unassigned"
    
    time.sleep(2)
    
    select.options[1].click()       
    
    time.sleep(2)
    
    driver.find_element(By.CLASS_NAME,"btn").click()
    
    time.sleep(1)
    
    sessionVar_Result = driver.find_element(By.CLASS_NAME,"sessionVars")
    
    time.sleep(1)
    
    sesVar_Value = sessionVar_Result.text
    
    time.sleep(1)
    
    select = Select(driver.find_element(By.ID,'companySelected'))
    
    theOptions = select.options  
    
    assert sesVar_Value != "0 tables updated"
    assert theOptions[0].get_attribute("value") != "Unassigned"
     
    time.sleep(2)
    
    select = Select(driver.find_element(By.ID,'assignmentSelected'))
    
    theOptions = select.options
    
    assert theOptions[0].get_attribute("value") == "Pending confirmation"
    
    time.sleep(2)
    
    select.options[2].click()       
    
    time.sleep(2)
    
    driver.find_element(By.CLASS_NAME,"btn").click()
    
    time.sleep(2)
    
    sessionVar_Result = driver.find_element(By.CLASS_NAME,"sessionVars")
    
    sesVar_Value = sessionVar_Result.text
    
    select = Select(driver.find_element(By.ID,'assignmentSelected'))
    
    theOptions = select.options
    
    time.sleep(2)  
    
    assert theOptions[0].get_attribute("value") == "Confirmed"    
    assert sesVar_Value != "0 tables updated"            

    time.sleep(2)
    
    select = Select(driver.find_element(By.ID,'assignmentSelected'))
    
    theOptions = select.options
    
    select.options[1].click() 
    
    time.sleep(2)
    
    driver.find_element(By.CLASS_NAME,"btn").click()        

    time.sleep(2)

    select = Select(driver.find_element(By.ID,'assignmentSelected'))
    
    theOptions = select.options

    assert theOptions[0].get_attribute("value") == "Unassigned"    
    assert sesVar_Value != "0 tables updated"
 
    time.sleep(2) 
    
    driver.quit()

def recursiveMatchStud():
    
    #driver = webdriver.Chrome \
    #    (service=ChromeService \
    #        (executable_path=ChromeDriverManager() \
    #            .install()))
    
    chrome_service = Service(ChromeDriverManager().install()) 
    
    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]       

    for option in options:
        chrome_options.add_argument(option)

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    
    driver.get("http://localhost:5221/Match_Student")
    
    time.sleep(1)
    
    title = driver.title
    assert title == "Match Students - My Webpage"
    
    time.sleep(1)
    
    return driver            