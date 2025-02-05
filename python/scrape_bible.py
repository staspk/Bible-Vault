import sys
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from definitions import *

book = 'Genesis'
chapter = 1
chosen_translations = ['kjv', 'nasb', 'rsv', 'rusv', 'nrt']

string = ';'.join(chosen_translations)
print(string)
sys.exit()

BIBLE_GATEWAY_URL = fr'https://www.biblegateway.com/passage/?search={book}{chapter}&version={version}'

GENESIS1 = fr'file://{PROJECT_ROOT_DIRECTORY}/genesis1.html'

opts = Options()
opts.add_argument("--headless")
driver = webdriver.Chrome(options=opts)
# driver = webdriver.Chrome()



driver.get(GENESIS1)

passageDiv = driver.find_element(By.CLASS_NAME, 'passage-text').get_attribute('innerHTML')

soup = BeautifulSoup(passageDiv, 'html.parser')

# for child in soup.descendants:
#     print(child)

print(passageDiv)

driver.quit()