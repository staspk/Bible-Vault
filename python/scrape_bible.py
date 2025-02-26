import sys
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from definitions import *

book = 'Genesis'
book = '1'
chapter = 1
us_translations = ['kjv', 'nkjv', 'esv', 'nasb', 'niv', 'rsv', 'nrsv', 'ylt']
rus_translations = ['rusv', 'nrt']
target_translation = 'RSV'

version_string = ';'.join(us_translations)
print(version_string)
# sys.exit()

# https://www.biblegateway.com/passage/?search=Genesis4&version=rsv
BIBLE_GATEWAY_URL = fr'https://www.biblegateway.com/passage/?search={book}{chapter}&version={target_translation}'

GENESIS1 = fr'file://{PROJECT_ROOT_DIRECTORY}/genesis1.html'

opts = Options()
opts.add_argument("--headless")
# opts.add_argument('--log-level=3')
driver = webdriver.Chrome(options=opts)
# driver = webdriver.Chrome()


driver.get(BIBLE_GATEWAY_URL)
passageTextDiv = driver.find_element(By.CLASS_NAME, 'passage-text')
html = passageTextDiv.get_attribute('outerHTML')
with open('toParse.html', 'w', encoding='utf-8') as file:
    file.write(html)

driver.get(TEMPORARY_HTML)
print(driver.page_source)

sys.exit()

curVerse = 1
htmlId = f'en-{target_translation}-{curVerse}'


soup = BeautifulSoup(driver.page_source, 'html.parser')
passageTextDiv = soup.find('div', class_='passage-text')
verse1 = soup.find('span', 'text Gen-1-1')

print(verse1)



# with open("soup.html", "w", encoding="utf-8") as file:
#     file.write(passageTextDiv.prettify())






driver.quit()