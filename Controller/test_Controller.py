import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

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

class WebTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the WebDriver
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        # Launch the webpage
        cls.driver.get(data["LoginURL"])          

    #Valid Case(both username and password are correct)
    def test_AvalidloginForm(self):

        wait = WebDriverWait(self.driver, 10)       

        #parse username
        username= wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username.send_keys(valid_data["UserName"])

        #parse password
        password = wait.until(EC.presence_of_element_located((By.NAME,"password")))
        password.send_keys(valid_data["Password"])

        #click Login button
        login = wait.until(EC.presence_of_element_located((By.XPATH,data["LoginPath"])))
        login.click()   
        
        #click the profile to logout
        profile = wait.until(EC.presence_of_element_located((By.XPATH,data["ProfilePath"])))
        profile.click()

        #click the logout button
        logout = wait.until(EC.presence_of_element_located((By.XPATH,data["LogoutPath"])))
        logout.click()

        time.sleep(5)   

    #Invalid Case(both username and password are incorrect)
    def test_invalidloginForm1(self):

        wait = WebDriverWait(self.driver, 10)       

        username= wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username.send_keys(invalid_data["InvalidUserName"])

        password = wait.until(EC.presence_of_element_located((By.NAME,"password")))
        password.send_keys(invalid_data["InvalidPassword"])

        login = wait.until(EC.presence_of_element_located((By.XPATH,data["LoginPath"])))
        login.click()

        time.sleep(5)   

    #Invalid Case(incorrect username and correct password)
    def test_invalidloginForm2(self):

        wait = WebDriverWait(self.driver, 10)       

        username= wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username.send_keys(invalid_data["InvalidUserName"])

        password = wait.until(EC.presence_of_element_located((By.NAME,"password")))
        password.send_keys(valid_data["Password"])

        login = wait.until(EC.presence_of_element_located((By.XPATH,data["LoginPath"])))
        login.click()

        time.sleep(5)   
                
    #Invalid Case(correct username and incorrect password)
    def test_invalidloginForm3(self):

        wait = WebDriverWait(self.driver, 10)       

        username= wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username.send_keys(valid_data["UserName"])

        password = wait.until(EC.presence_of_element_located((By.NAME,"password")))
        password.send_keys(invalid_data["InvalidPassword"])

        login = wait.until(EC.presence_of_element_located((By.XPATH,data["LoginPath"])))
        login.click()

        time.sleep(5)            
          

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
