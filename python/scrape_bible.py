import sys
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from definitions import *
from kozubenko.io import load_file, remove_html_tags
from kozubenko.os import File
from models.Bible import BIBLE, Book
from python.kozubenko.time import Time
from python.kozubenko.utils import Utils

def report_exception(report:str):
    FILE = File(REPORTS_DIRECTORY, 'exceptions', file=Time.utc_now)

    
    
    pass

def scrape_basic_html(book:Book, target_translation = 'RSV', start_chapter = 1):
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)

    for chapter in range(start_chapter, book.chapters + 1):
        try:
            FILE = fr'{BIBLE_HTML}\{target_translation}\{book.name}\{chapter}.html'
            BIBLE_GATEWAY = fr'https://www.biblegateway.com/passage/?search={book.abbr}{chapter}&version={target_translation}'
            
            driver.get(BIBLE_GATEWAY)

            passageTextDiv = driver.find_element(By.CLASS_NAME, 'passage-text')
            html = passageTextDiv.get_attribute('outerHTML')

            os.makedirs(os.path.dirname(FILE), exist_ok=True)
            with open(FILE, 'w', encoding='utf-8') as file:
                file.write(html)

            time.sleep(20)
            time.sleep(Utils.random_int(5, 15))
        except Exception as e:
            type(e).__name__
            report = ''
            report



def scrape_rsv_html(book:Book):
    """
    folder_path: path to folder holding the books chapters. file names should be:
    - 1.html
    - 2.html
    - 3.html
    - etc.
    """
    
    for chapter in range(1, book.chapters):
        FILE = fr'{BIBLE_HTML}\{book.name}\{chapter}.html'
        html_str = load_file(FILE)


        new_str = remove_html_tags(html_str)

        print_yellow(new_str)
        print('\n\n')

        if chapter == 3:
            raise Exception

        # TARGET_1 = f'{chapter}&nbsp;</span>'                            # delimiter, verse1 text is right after
        # split_str = html_str.split(TARGET_1, 1)
        
        # print_yellow(split_str[0])


def soup_scrape(book:Book, start_chapter = 1):
    for chapter in range(start_chapter, book.chapters + 1):
        READ_FILE = fr'{BIBLE_HTML}\{book.name}\{chapter}.html'
        WRITE_FILE = fr'{BIBLE_TXT}\{book.name}\{chapter}.txt'
        with open(READ_FILE, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        spans = soup.find_all("span", class_=lambda x: x.startswith(f"text"))
        footnotes = soup.find("div", class_="footnotes")

        for span in spans:
            print_yellow(span.get_text())
        for note in footnotes:
            print_yellow(note.get_text())
        print('\n')

        os.makedirs(os.path.dirname(WRITE_FILE), exist_ok=True)
        with open(WRITE_FILE, 'w', encoding='utf-8') as file:
            for span in spans:
                file.write(span.get_text() + '\n')
            for footnote in footnotes:
                file.write(note.get_text() + '\n')
        
        # if chapter == 10:
        #     raise Exception

def soup_second_pass(book:Book):
    for chapter in range(1, book.chapters):
        FILE = fr'{BIBLE_TXT}\{book.name}\{chapter}.txt'

        with open(FILE, 'r', encoding='utf-8') as file:
            html_content = file.read()

        

def selenium_scrape(book:Book):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        for chapter in range(1, book.chapters):
            FILE = fr'{BIBLE_HTML}\{book.name}\{chapter}.html'
            print_red(FILE)
            driver.get(FILE)

            text = driver.find_element(By.TAG_NAME, "div").text
            text = driver.execute_script(
                "return document.body ? document.body.innerText : document.documentElement.innerText;"
            )

            print_yellow(text)

            raise Exception
    finally:
        driver.quit()


if __name__ == "__main__":
    book = 'Genesis'
    # book = '1'
    chapter = 1
    us_translations = ['kjv', 'nkjv', 'esv', 'nasb', 'niv', 'rsv', 'nrsv', 'ylt']
    rus_translations = ['rusv', 'nrt']
    target_translation = 'RSV'

    version_string = ';'.join(us_translations)
    print(version_string)

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

    curVerse = 1
    htmlId = f'en-{target_translation}-{curVerse}'


    soup = BeautifulSoup(driver.page_source, 'html.parser')
    passageTextDiv = soup.find('div', class_='passage-text')
    verse1 = soup.find('span', 'text Gen-1-1')

    print(verse1)

    driver.quit()