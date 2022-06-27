from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import os

load_dotenv()   # load environment variables
DRIVER_PATH = 'chromedrivers/chromedriver_mac64'

options = Options()
options.headless = False
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get('https://worldcubeassociation.org')

signin_hover = driver.find_element_by_xpath('/html/body/div[1]/div[2]/ul[2]/li[3]/a')
signin = driver.find_element_by_xpath('/html/body/div[1]/div[2]/ul[2]/li[3]/ul/li[1]/a')
actions = ActionChains(driver)
actions.move_to_element(signin_hover)
actions.click(signin).pause(4)
actions.perform()

# username = WebDriverWait(driver, 5).until(
#     EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[2]/div/div[2]/form/div[1]/input')) )
username = driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/form/div[1]/input')
password = driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/form/div[2]/input')
username.send_keys(os.environ['username'])
password.send_keys(os.environ['password'])
driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/form/input[3]').click()
ActionChains(driver).pause(3).perform()

driver.quit()