from dataclasses import dataclass
from typing import Union
import random, time, traceback
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from definitions import *
from kozubenko.io import load_file, remove_html_tags
from kozubenko.os import File
from kozubenko.print import *
from kozubenko.time import Time, Timer
from tor.tor import Tor
from kozubenko.utils import AssertClass, AssertList, Utils
from models.Bible import Book
from user_agents import random_user_agent


@dataclass
class BibleGatewayOption:
    state:bool
    element:WebElement

    def __post_init__(self):
        if type(self.state) is not bool or not isinstance(self.element, WebElement):
            raise Exception(f"BibleGatewayOption(state:bool, element:WebElement) -> constructor error: types are enforced")

    def set_state(self, state:bool):
        if type(self.state) is not bool:
            raise Exception(f"BibleGatewayOption.set_state(self, state:bool) -> state must be a bool")
        
        if self.state != state:
            self.state = state
            self.element.click()       

@dataclass
class BibleGatewayOptions:
    cross_references: BibleGatewayOption
    footnotes       : BibleGatewayOption
    verse_numbers   : BibleGatewayOption
    headings        : BibleGatewayOption
    red_letter      : BibleGatewayOption

    def __post_init__(self):
        if any(not isinstance(instance_var_value, BibleGatewayOption) for instance_var_value in self.__dict__.values()):
            raise Exception(f"BibleGatewayOptions(*args:BibleGatewayOption) -> constructor error: types are enforced")
        
    def __str__ (self) -> str:
        return (
            f"cross_references: {self.cross_references.state}\n"
            f"footnotes: {self.footnotes.state}\n"
            f"verse_numbers: {self.verse_numbers.state}\n"
            f"headings: {self.headings.state}\n"
            f"red_letter: {self.red_letter.state}"
        )

    def cross_references(self, state:bool):
        self.cross_references.set_state(bool(state))

    def footnotes(self, state:bool):
        self.footnotes.set_state(bool(state))

    def verse_numbers(self, state:bool):
        self.verse_numbers.set_state(bool(state))

    def headings(self, state:bool):
        self.headings.set_state(bool(state))

    def red_letter(self, state:bool):
        self.red_letter.set_state(bool(state))

    def set_states(self, cross_references:bool = None, footnotes:bool = None, verse_numbers:bool = None, headings:bool = None, red_letter:bool = None):
        if cross_references is not None:
            self.cross_references.set_state(bool(cross_references)) 
        if footnotes is not None:
            self.footnotes.set_state(bool(footnotes)) 
        if verse_numbers is not None:
            self.verse_numbers.set_state(bool(verse_numbers))
        if headings is not None:
            self.headings.set_state(bool(headings))
        if red_letter is not None:
            self.red_letter.set_state(bool(red_letter))
    

def report_exception(exception:Exception):
    FILE = File(REPORTS_DIRECTORY, 'exceptions', file=Time.local_time_as_legal_filename())

    exception_type = type(exception).__name__
    exception_message = str(exception)
    exception_trace = traceback.format_exc()

    report = f"Exception Type: {exception_type}\\n"
    report += f"Message: {exception_message}\\n\\n"
    report += f"Traceback:\\n{exception_trace}"

    with open(FILE, 'w', encoding='UTF-8') as file:
        file.write(report)



def scrape_bible(book:Book, target_translations:list):
    """
    supported len(target_translations): 1-5
    """
    AssertClass("book", book, Book)
    AssertList("target_translations", target_translations, min_len=1, max_len=5)

    print_green(f"scrape_bible({book}, {target_translations})")

    TOR = Tor()
    for chapter in range(2, book.chapters):
        URL = fr"https://www.biblegateway.com/passage/?search={book.abbr}%20{chapter}&version={Utils.list_to_str(target_translations, ';')}"

        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.socks", "127.0.0.1")
        profile.set_preference("network.proxy.socks_port", TOR._socks_port)
        profile.set_preference("network.proxy.socks_remote_dns", True)
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)

        page_options_checkboxes = Options()
        page_options_checkboxes.profile = profile
        # options.headless = True

        driver = webdriver.Firefox(options=page_options_checkboxes)

        driver.get(URL)

        settings_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.settings"))
        )
        time.sleep(1.25)
        settings_icon.click()

        settings_div = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".bg-tooltip.options-tooltip"))
        )
        page_options_checkboxes = settings_div.find_elements(By.CSS_SELECTOR, "div[style*='cursor: pointer;'] svg")
        page_options_toggles    = settings_div.find_elements(By.CSS_SELECTOR, "div[style*='cursor: pointer;']")
        page_options_states     = [True if svg.get_attribute("name") == 'checked' else False for svg in page_options_checkboxes]
        page_options_states_and_toggles = [BibleGatewayOption(state, toggle) for state, toggle in zip(page_options_states, page_options_toggles)]
        page_options                    = BibleGatewayOptions(*page_options_states_and_toggles)

        page_options.set_states(False, False, True, False, True)
        settings_icon.click()

        with open('./temporary.html', 'w', encoding='UTF-8') as file:
            file.write(driver.page_source)

        time.sleep(6000)

        driver.quit()
        TOR.stop()
        exit()


def stealth_scrape_chapter(book:Book, chapter:int, translations:list[str]):
    with Tor() as tor:
        for translation in translations:
            print_red(f'stealth_scrape_chapter called on: {book.name}:{chapter}; translation: {translation}')
            try:
                URL = fr'https://www.biblegateway.com/passage/?search={book.abbr}{chapter}&version={translation}'
                HTML = File(BIBLE_HTML, translation, book.name, file=f'{chapter}.html')

                response = requests.get(URL, headers=random_user_agent(), proxies=tor.proxies_as_dict())

                soup = BeautifulSoup(response.text, "html.parser")
                passage_div = soup.find("div", class_="passage-text")

                with open(HTML, 'w', encoding='UTF-8') as file:
                    file.write(str(passage_div))

            except Exception as e:
                report_exception(e)

def stealth_scrape_one(book:Book, target_translation:str, chapter:int):
    with Tor() as tor:
        try:
            URL = fr'https://www.biblegateway.com/passage/?search={book.abbr}{chapter}&version={target_translation}'
            SAVED_HTML = File(BIBLE_HTML, target_translation, book.name, file=f'{chapter}.html')
            TXT_FILE  = File(BIBLE_TXT, target_translation, book.name, file=f'{chapter}.html')

            print_red(f'stealth_scrape_one called on: {URL}')

            response = requests.get(URL, headers=random_user_agent(), proxies=tor.proxies_as_dict())

            soup = BeautifulSoup(response.text, "html.parser")
            passage_div = soup.find("div", class_="passage-text")

            with open(SAVED_HTML, 'w', encoding='UTF-8') as file:
                file.write(str(passage_div))

        except Exception as e:
            report_exception(e)

def stealth_scrape(book:Book, target_translation:Union[str, list[str]], start_chapter = 1):
    if type(target_translation) is str:
        target_translation = [target_translation]

    TOR = Tor()

    for translation in target_translation:
        for chapter in range(start_chapter, book.chapters + 1):
            try:
                FILE = File(BIBLE_HTML, translation, book.name, file=f'{chapter}.html')
                URL = fr'https://www.biblegateway.com/passage/?search={book.abbr}{chapter}&version={translation}'

                print_red(URL)

                # opts = Options()
                # opts.add_argument(f"user-agent={user_agent}")

                response = requests.get(URL, headers=random_user_agent(), proxies=TOR.proxies_as_dict())

                soup = BeautifulSoup(response.text, "html.parser")
                passage_div = soup.find("div", class_="passage-text")

                with open(FILE, 'w', encoding='UTF-8') as file:
                    file.write(str(passage_div))

                time.sleep(random.randint(0, 5))

            except Exception as e:
                report_exception(e)

    TOR.stop()



def scrape_basic_html(book:Book, target_translation = 'RSV', start_chapter = 1):
    opts = Options()
    opts.add_argument("--headless")
    
    driver = webdriver.Chrome(options=opts)

    for chapter in range(start_chapter, book.chapters + 1):
        try:
            FILE = File(BIBLE_HTML, target_translation, book.name, file=f'{chapter}.html')
            BIBLE_GATEWAY = fr'https://www.biblegateway.com/passage/?search={book.abbr}{chapter}&version={target_translation}'
            
            driver.get(BIBLE_GATEWAY)

            passageTextDiv = driver.find_element(By.CLASS_NAME, 'passage-text')
            html = passageTextDiv.get_attribute('outerHTML')

            with open(FILE, 'w', encoding='utf-8') as file:
                file.write(html)

            time.sleep(20)
            time.sleep(Utils.random_int(5, 15))
        except Exception as e:
            exception_type = type(e).__name__
            exception_message = str(e)
            exception_trace = traceback.format_exc()

            report = f"Exception Type: {exception_type}\\n"
            report += f"Message: {exception_message}\\n\\n"
            report += f"Traceback:\\n{exception_trace}"
            report_exception(report)



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

    # chrome_options.add_argument('--proxy-server=socks5h://127.0.0.1:9050')

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