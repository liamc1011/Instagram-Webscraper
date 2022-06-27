from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DRIVER_PATH = 'chromedrivers/chromedriver_mac64'

options = Options()
options.headless = False
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get('https://google.com')