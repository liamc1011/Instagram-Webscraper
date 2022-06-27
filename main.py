from distutils.log import debug
from prettytable.prettytable import ALL, FRAME
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from contextlib import redirect_stdout
import getpass
import sys
import prettytable
import account # account.py

# path to find chromedriver (same directory)
DRIVER_PATH = 'chromedrivers/chromedriver'
# global driver var
driver = None

LONG_TIMEOUT = 20
MID_TIMEOUT = 6

# global username of the account you want to scrape
target_accnt = ''
accounts = {}

# global option variables (used when running script from command line)
head = False
tfa = False
debugg = False
file = False

def start():
    options = Options()
    if head == False: # global headful or headless option 
        options.headless = True
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--incognito")
    # User agent to bypass Instagram's webscraper detection. Might want to add more in case they up their game
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    
    global driver
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get('https://instagram.com/')

# Login to Instagram.com
def login():
    username_field = WebDriverWait(driver, LONG_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]//input[@name="username"]')) )
    password_field = WebDriverWait(driver, LONG_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]//input[@name="password"]')) )
    login = WebDriverWait(driver, LONG_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="loginForm"]//button//*[text()="Log In"]')) )
    username = input('Enter Instagram username: ')
    password = getpass.getpass('Enter Instagram password: ')
    username_field.send_keys(username)
    password_field.send_keys(password)
    login.click()


# If 2 Factor Authentication on, with authentication app
def two_factor_app():
    security_code = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]//input[@aria-label="Security Code"]')) )
    confirm_btn = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]//button[text()="Confirm"]')) )
    verif_code_descr = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'verificationCodeDescription')) )

    # insert try/except if user misinputs
    print('Via https://instagram.com: ')
    print(verif_code_descr.text[:-1] + ': ', end='')
    verification_code = input()

    # If takes too long to input code then StaleElementReference is thrown, just relocate the element
    try: 
        security_code.send_keys(verification_code)
    except StaleElementReferenceException:
        security_code = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]//input[@aria-label="Security Code"]')) )
        confirm_btn = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]//button[text()="Confirm"]')) )
        security_code.send_keys(verification_code)

    confirm_btn.click()


# Checks if logged in successfully
def login_success():
    try:
        # Checks for presence of home button, which indicates successful login
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//nav//*[@aria-label="Home"]')) )
        # Checks for presence of explore button, which indicates successful login
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//nav//*[@aria-label="Find People"]')) )
        # Checks for presence of activity button, which indicates successful login
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//nav//*[@aria-label="Activity Feed"]')) )
        # Checks for presence of your avatar, which indicates successful login
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//nav//img[@data-testid="user-avatar"]')) )
    except (TimeoutException) as e:
        print('Error logging in')
        print(e)
    else: 
        print('Logged in successfully')


# Choose to not save login information on the popup
def login_info_popup():
    try: 
        # Checks for presence of "save info" button, which indicates presence of save login info popup
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]//button[text()="Save Info"]')) )
        save_login_not_now = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]//button[text()="Not Now"]')) )
        # assertion for element containing "Save login information?"
    except (TimeoutException, AssertionError):
        print("No save login info popup")
    else: 
        save_login_not_now.click()


# Choose to not turn on notifications on the popup
def notifs_popup():
    try:
        # Checks for presence of "turn on" button, which indicates presence of the notifs popup
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@role="dialog"]//button[text()="Turn On"]')) )
        notifs_not_now = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@role="dialog"]//button[text()="Not Now"]')) )    
        # assertion for element containing "Turn on notifications"
    except (TimeoutException, AssertionError):
        print("No notification popup")
    else:
        notifs_not_now.click()


def visit_own_profile():
    avatar = driver.find_element(By.XPATH, '//nav//img[@data-testid="user-avatar"]')
    avatar.click()
    profile = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//nav//div[text()="Profile"]')) )
    profile.click()


def visit_profile():
    global target_accnt
    target_accnt = input("\nWho's follower/following do you want to scrape? Enter their Instagram username." +
            "\nPlease note that scraping accounts that are not your own will result in slight inaccuraccies with the data." + 
            "\nThis is because Instagram's website omits a small amount of people from the follower/following list if the account is not your own." +
            "\nInstagram username: ")
    driver.get('https://instagram.com/' + target_accnt)


def get_followers():
    try:
        followers = WebDriverWait(driver, MID_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, '//header//ul//a')) )
    except (TimeoutException):
        print("Cannot access user's follower list. They may be private and you don't follow them.")
        return 
    num_followers_text = followers.find_element(By.XPATH, './/span')
    print(f"Wow you have {num_followers_text.text} followers! Not bad :)")
    num_followers = to_int(num_followers_text.text)
    followers.click()
    follower_panel = WebDriverWait(driver, MID_TIMEOUT).until(
            # EC.visibility_of_element_located((By.XPATH, '//body//div[@aria-label="Followers"]')) )
            EC.visibility_of_element_located((By.XPATH, '//body//div[@role="dialog"]')) )
    # wait for followers to load
    ActionChains(driver).pause(3).perform()
    
    # scrolling until reach the bottom of followers list
    print('Looking through followers...', end='.')
    
    follower_username_list = []
    follower_name_list = None
    curr_length = 0
    prev_length = -1
    list_length_unchanged = 0

    while (curr_length < num_followers and list_length_unchanged < 10):
        if (prev_length == curr_length):
            list_length_unchanged += 1
        else:
            list_length_unchanged = 0

        try:
            ActionChains(driver).move_to_element( follower_panel.find_element(By.XPATH, './/li[last()]') ).perform()    #try except?
        except StaleElementReferenceException:
            ActionChains(driver).move_to_element( follower_panel.find_element(By.XPATH, './/li[last()]') ).perform()
        
        prev_length = curr_length
        follower_username_list = follower_panel.find_elements(By.XPATH, './/li//span[1]/a') # a in first span of the li's will get you the username
        curr_length = len(follower_username_list)
        if debugg: # if running this program in debugging mode 
            print(f"len of list {len(follower_username_list)}") # testing purposes
        
    follower_name_list = follower_panel.find_elements(By.XPATH, './/li//span[1]/../following-sibling::*') # DOM changes after loading more followers
    print(f"follower number: {len(follower_username_list)}")
    print('.......done')
    print('Adding objects...', end='.')
    global accounts
    for username, name in zip(follower_username_list, follower_name_list):
        accounts[username.text] = account.Account(username.text, name.text, follows_you=True)
    print('.......done')

    close = driver.find_element(By.XPATH, '//button//*[@aria-label="Close"]')
    close.click()
        

def get_following():
    try:   
        following = WebDriverWait(driver, MID_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, '//header//ul//li[last()]')) )
    except (TimeoutException):
        print("Cannot access user's following list. They may be private and you don't follow them.")
        return
    num_following_text = following.find_element(By.XPATH, './/span')
    print(f"You're following {num_following_text.text} people! Loserr")
    num_following = to_int(num_following_text.text)
    following.click()
    following_panel = WebDriverWait(driver, MID_TIMEOUT).until(
            # EC.visibility_of_element_located((By.XPATH, '//body//div[@aria-label="Following"]')) )
            EC.visibility_of_element_located((By.XPATH, '//body//div[@role="dialog"]')) )
    # wait for following to load
    ActionChains(driver).pause(3).perform()

    # scrolling until reach the bottom of following list
    print('Looking through following...', end='.')

    following_username_list = []
    following_name_list = None
    curr_length = 0
    prev_length = -1
    list_length_unchanged = 0

    while(len(following_username_list) < num_following and list_length_unchanged < 10):
        if (prev_length == curr_length):
            list_length_unchanged += 1
        else:
            list_length_unchanged = 0

        try:
            ActionChains(driver).move_to_element( following_panel.find_element(By.XPATH, './/li[last()]') ).perform()    #try except?
        except StaleElementReferenceException:
            ActionChains(driver).move_to_element( following_panel.find_element(By.XPATH, './/li[last()]') ).perform()
        
        prev_length = curr_length
        following_username_list = following_panel.find_elements(By.XPATH, './/li//span[1]/a') # a in first span of the li's will get you the username
        curr_length = len(following_username_list)
        if debugg: # if running this program in debugging mode 
            print(f"len of list {len(following_username_list)}")
        
    following_name_list = following_panel.find_elements(By.XPATH, './/li//span[1]/../following-sibling::*') # DOM changes after loading more followers
    print(f"following number: {len(following_username_list)}")
    print('.......done')
    print('Adding objects...', end='.')
    global accounts
    for username, name in zip(following_username_list, following_name_list):
        if (username.text in accounts):
            accounts[username.text].you_follow = True
        else:
            accounts[username.text] = account.Account(username.text, name.text, follows_you=False, you_follow=True)
    print('.......done')       

def webelements_to_text(webelements):
    text_list = []
    for webelement in webelements:
        text_list.append(webelement.text)
    return text_list

def to_int(number):
    number = number.replace(',','') # remove all commas
    return int(number)

def make_table():
    doesnt_follow_you_back = 0
    you_dont_follow_back = 0
    follow_each_other = 0

    table = prettytable.PrettyTable()
    table.field_names = ['Name', 'They Follow You', 'You Follow Them']
    for account in accounts.values():
        curr_account = accounts[account.username]
        if (curr_account.follows_you==False and curr_account.you_follow==True):
            table.add_row([f"{account.username} ({account.name})", account.follows_you, account.you_follow])
            doesnt_follow_you_back += 1
    # poor man's sorting (three passes)
    for account in accounts.values():
        curr_account = accounts[account.username]
        if (curr_account.follows_you==True and curr_account.you_follow==False):
            table.add_row([f"{account.username} ({account.name})", account.follows_you, account.you_follow])
            you_dont_follow_back += 1
    for account in accounts.values():
        curr_account = accounts[account.username]
        if (curr_account.follows_you==True and curr_account.you_follow==True):
            table.add_row([f"{account.username} ({account.name})", account.follows_you, account.you_follow])
            follow_each_other += 1
    
    if file == True: 
        with open('output.txt', 'w') as redirect:
            with redirect_stdout(redirect):
                print_table(table, doesnt_follow_you_back, you_dont_follow_back, follow_each_other)
    else:
        print()
        print_table(table, doesnt_follow_you_back, you_dont_follow_back, follow_each_other)

def print_table(table, doesnt_follow_you_back, you_dont_follow_back, follow_each_other):
    print(f"People who don't follow you back: {doesnt_follow_you_back}")
    print(f"People you don't follow back: {you_dont_follow_back}")
    print(f"People that you follow and they follow you back: {follow_each_other}")
    print(table)

def options(args):
    if "--tfa" in args:
        global tfa
        tfa = True
    if "--debug" in args:
        global debugg
        debugg = True
    if "--head" in args:
        global head
        head = True
    if "--file" in args:
        global file
        file = True

def main():
    options(sys.argv) # Configures options
    start() # Starts Selenium Webdriver
    login() # Login to Instagram.com
    if tfa: 
        two_factor_app() # Only if 2FA option is passed in when running
    login_success() # Checks if logged in successfully
    visit_profile()
    get_followers()
    get_following()
    make_table()
    driver.quit()


if __name__ == '__main__':
    main()
