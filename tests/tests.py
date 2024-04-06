from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

opts = webdriver.ChromeOptions()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
#opts.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=opts)
url = "http://172.31.34.164"

def test_reachable():
    response = requests.get(url)
    assert response.status_code == 200, "Website is reachable"
    

def test_positive_location_found():
    driver.get(url)
    element = driver.find_element(By.NAME, 'location')
    element.send_keys("israel")
    element.submit()
    # buttun_s = driver.find_element(By.XPATH, "//button[text()='Get Weather']")
    # buttun_s.click()
    assert '/weather' in driver.current_url, "Failed to find the location"


def test_negetive_location_found():
    driver.get(url)
    element = driver.find_element(By.NAME, 'location')
    element.send_keys("notisrsa")
    buttun_s = driver.find_element(By.XPATH, "//button[text()='Get Weather']")
    buttun_s.click()
    error = driver.find_element(By.XPATH, "//*[contains(text(), 'was not found')]")
    assert error
