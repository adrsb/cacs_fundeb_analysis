import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def start_chrome_driver() -> webdriver.Chrome:
    """
    Inicia o Chrome WebDriver usando o WebDriver Manager.
    """
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def click_element_by_xpath(driver: webdriver.Chrome, xpath: str, wait: int = 5):
    """
    Clica em um elemento localizado por XPath.
    """
    element = driver.find_element(by="xpath", value=xpath)
    element.click()
    time.sleep(wait)
