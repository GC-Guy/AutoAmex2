# helper files for amex automation

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv
import time

# Constants
offer_page = "https://global.americanexpress.com/offers/eligible"
added_page = "https://global.americanexpress.com/offers/enrolled"
amexWebsite = "https://online.americanexpress.com/myca/logon/us/action/LogonHandler?request_type=LogonHandler&Face=en_US&inav=iNavLnkLog"
amexWebsite15 = "https://online.americanexpress.com/myca/logon/us/action?request_type=LogonHandler&Face=en_US&DestPage=https%3A%2F%2Fonline.americanexpress.com%2Fmyca%2Facctmgmt%2Fus%2Fmyaccountsummary.do%3Frequest_type%3Dauthreg_acctAccountSummary%26Face%3Den_US%26pageView%3Djanus%26omnlogin%3Dus_homepage_myca"

def loadConfig(filename):
    ''' load your config.csv file
        the file should contain username, password, and optionally
        last 5 digits and nickname for cc in each line
        make sure the file is under the same directory '''
    username = []
    password = []
    lastfive = []
    nickname = []
    try:
        f = open(filename, 'rb')
        reader = csv.reader(f)
        for row in reader:
            username.append(row[0])
            password.append(row[1])
            try: lastfive.append(row[2])
            except: lastfive.append('')
            try: nickname.append(row[3])
            except: nickname.append('')
        f.close()
    except:
        print("file read failed...Confirm your CSV includes newline (excel for mac does not by default)")
    return username, password, lastfive, nickname

def getDriver(browser):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1440,900")
    if browser.lower() == 'firefox':
        driver = webdriver.Firefox()
    elif browser.lower() == 'chrome':
        driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    elif browser.lower() == 'chrome_linux':
        driver = webdriver.Chrome('./chromedriver_linux64', chrome_options=chrome_options)
    elif browser.lower() in ('phantomjs', 'headless'):
        driver = webdriver.PhantomJS()
    else:
        print("WARNING: browser selection not valid, use PhantomJS as default")
        driver = webdriver.PhantomJS()
    return driver

def amexLogIn(driver, usr, pwd):
    emailFieldID = "eliloUserID"
    passFieldID = "eliloPassword"
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(emailFieldID) ).clear()
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(emailFieldID) ).send_keys(usr)
    time.sleep(1)
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(passFieldID) ).clear()
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(passFieldID) ).send_keys(pwd)
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name("btn-fluid") ).click()


def amexLogOut(driver):
    WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_class_name("btn-secondary")).click()



