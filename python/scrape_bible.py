import sys
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from definitions import *

book = 'Genesis'
book = '2Kgs'
chapter = 4
us_translations = ['kjv', 'nkjv', 'esv', 'nasb', 'niv', 'rsv', 'nrsv', 'ylt']
rus_translations = ['rusv', 'nrt']
target_translation = 'rsv'

version_string = ';'.join(us_translations)
print(version_string)
# sys.exit()

# https://www.biblegateway.com/passage/?search=Genesis4&version=rsv
BIBLE_GATEWAY_URL = fr'https://www.biblegateway.com/passage/?search={book}{chapter}&version={target_translation}'

GENESIS1 = fr'file://{PROJECT_ROOT_DIRECTORY}/genesis1.html'

opts = Options()
# opts.add_argument("--headless")
driver = webdriver.Chrome(options=opts)
# driver = webdriver.Chrome()



driver.get(BIBLE_GATEWAY_URL)


passageDiv = driver.find_element(By.CLASS_NAME, 'passage-text').get_attribute('innerHTML')

passageText = driver.find_element(By.CLASS_NAME, 'passage-text').text

soup = BeautifulSoup(passageDiv, 'html.parser')

# for child in soup.descendants:
#     print(child)

# print(passageDiv)
print(passageText)

driver.quit()