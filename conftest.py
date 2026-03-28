import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from urls import stellarburgers_URL 

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    
    driver = webdriver.Chrome(options=options)
    
    driver.get(stellarburgers_URL)
    
    yield driver
    
    driver.quit()