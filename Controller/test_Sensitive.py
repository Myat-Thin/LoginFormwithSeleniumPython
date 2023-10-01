
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

#Get the current directory
cur_dir = os.path.dirname(os.path.realpath(__file__))

#construct the path to config.json using a relative path
conf_path = os.path.join(cur_dir, '..', 'config.json')

#Load the data from config.json file
try:
    with open(conf_path, "r") as config_file:
        data = json.load(config_file)
        # Access the "Valid" section
        valid_data = data.get('Valid') 
        # Access the "Invalid" section
        invalid_data = data.get('Invalid') 
except FileNotFoundError:
    print(f"Error: {conf_path} not found") 
    data = None  


@pytest.fixture
def driver():
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
    yield driver
    driver.quit()

     
def test_username_field(driver):   

    driver.get(data["LoginURL"])

    wait = WebDriverWait(driver, 10)      


    # Get the value of the username field and convert it to lowercase
    actual_username = valid_data["UserName"].lower()    #admin    

    expected_username = valid_data["UserName"] # Admin

    username= wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username.send_keys(actual_username)

    #parse password
    password = wait.until(EC.presence_of_element_located((By.NAME,"password")))
    password.send_keys(valid_data["Password"])

    login = wait.until(EC.presence_of_element_located((By.XPATH,data["LoginPath"])))
    login.click()

    time.sleep(5) 

    # Assertion: Check if the actual username matches the expected value "Admin"
    assert actual_username == expected_username, f"Expected '{expected_username}', but found '{actual_username}'"

    

