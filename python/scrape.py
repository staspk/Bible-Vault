from __future__ import annotations
from dataclasses import dataclass, fields
from datetime import datetime

import time, traceback

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from definitions import *
from kozubenko.os import File
from kozubenko.print import *
from kozubenko.time import Time
from kozubenko.utils import assert_bool, assert_class, assert_int, assert_list, assert_str, Utils
from tor.tor import Tor
from models.Bible import BIBLE, Book


@dataclass
class ProblemChapter:
    translation:str
    book:Book
    chapter:int
    dt:datetime

    def __post_init__(self):
        assert_str("translation", self.translation)
        assert_class("book", self.book, Book)
        assert_int("chapter", self.chapter, min_val=1)

    def __str__(self) -> str:
        return (
            f"Problem Chapter Collision Time: {str(self.dt)}\n"
            f"{self.book.name}:{self.chapter} [{self.translation}]"
        )
        

@dataclass
class BibleGatewayOption:
    state:bool
    element:WebElement

    def __post_init__(self):
        assert_bool("state", self.state)
        assert_class("element", self.element, WebElement)

    def set_state(self, state:bool):
        assert_bool("state", state)
        
        if self.state != state:
            self.state = state
            self.element.click()
            time.sleep(.1)

@dataclass
class BibleGatewayOptions:
    """
    How to Use:
     `page_options = BibleGatewayOptions.WebDriveInstructionsToFindMe(driver)`
     `page_options.set_states()`
    """
    cross_references: BibleGatewayOption
    footnotes       : BibleGatewayOption
    verse_numbers   : BibleGatewayOption
    headings        : BibleGatewayOption
    red_letter      : BibleGatewayOption

    settings_icon   : WebElement = None

    def __post_init__(self):
        for field in fields(self):
            if field.name == "settings_icon":
                continue
            value = getattr(self, field.name)
            assert_class(field.name, value, BibleGatewayOption)
    
    @classmethod
    def DriverInstructionsToFindMe(cls, driver:RemoteWebDriver) -> BibleGatewayOptions:
        """
        Static Constructor
        """
        cls.settings_icon = WebDriverWait(driver, 10).until(            # operation time avg: ~15ms
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.settings"))
        )
        time.sleep(1)
        cls.settings_icon.click()

        settings_div = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".bg-tooltip.options-tooltip"))
        )
        page_options_checkboxes = settings_div.find_elements(By.CSS_SELECTOR, "div[style*='cursor: pointer;'] svg")
        page_options_toggles    = settings_div.find_elements(By.CSS_SELECTOR, "div[style*='cursor: pointer;']")
        page_options_states     = [True if svg.get_attribute("name") == 'checked' else False for svg in page_options_checkboxes]
        page_options_states_and_toggles = [BibleGatewayOption(state, toggle) for state, toggle in zip(page_options_states, page_options_toggles)]
        page_options                    = cls(*page_options_states_and_toggles)

        return page_options
    
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

        BibleGatewayOptions.settings_icon.click()
        time.sleep(.33)

    def __str__ (self) -> str:
        return (
            f"cross_references: {self.cross_references.state}\n"
            f"footnotes: {self.footnotes.state}\n"
            f"verse_numbers: {self.verse_numbers.state}\n"
            f"headings: {self.headings.state}\n"
            f"red_letter: {self.red_letter.state}"
        )


def report_exception_and_EXIT(exception:Exception=None, report:str=None):
    FILE = File(REPORTS_DIRECTORY, 'exceptions', file=Time.local_time_as_legal_filename())

    if exception is not None and isinstance(exception, Exception):
        exception_type = type(exception).__name__
        exception_message = str(exception)
        exception_trace = traceback.format_exc()

        report = f"Exception Type: {exception_type}\n"
        report += f"Message: {exception_message}\n"
        report += f"Traceback:\n{exception_trace}"

    with open(FILE, 'w', encoding='UTF-8') as file:
        file.write(report)
    
    print_dark_red(f"See exception report at: {FILE}")
    print_dark_red('Stopping Program...')
    exit()

def scrape_bible_book(book:Book, target_translations:list[str], startChapter = 1) -> list[ProblemChapter]:
    """
    * target_translations: supported length: 1-5
    """
    assert_class("book", book, Book)
    assert_list("target_translations", target_translations, min_len=1, max_len=5)
    assert_int("startChapter", startChapter, min_val=1, max_val=book.chapters)

    TOR = Tor()
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.socks", "127.0.0.1")
    profile.set_preference("network.proxy.socks_port", TOR._socks_port)
    profile.set_preference("network.proxy.socks_remote_dns", True)
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)

    options = Options()
    options.profile = profile
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)

    problem_chapters: list[ProblemChapter] = []
    for chapter in range(startChapter, book.chapters+1):
        URL = fr"https://www.biblegateway.com/passage/?search={book.abbr}%20{chapter}&version={Utils.list_to_str(target_translations, ';')}"

        driver.get(URL)

        try:
            page_options = BibleGatewayOptions.DriverInstructionsToFindMe(driver)
            page_options.set_states(False, False, True, False, True)
        except:
            page_options = BibleGatewayOptions.DriverInstructionsToFindMe(driver)
            time.sleep(.1)
            page_options.set_states(False, False, True, False, True)

        max_verse = BIBLE.find_max_verse(book, chapter)
        for translation in target_translations:
            OUT_TXT = File(BIBLE_TXT, translation, book.name, file=f'{chapter}.txt')

            css_selector = f"[class*='version-{translation}'][class*='result-text-style-normal'][class*='text-html']"
            element = driver.find_element(By.CSS_SELECTOR, css_selector)

            try:
                chapter_text = element.text.replace('\n', '')

                split_text = chapter_text.split(' ', 1)
                if int(split_text[0]) != chapter:
                    report_exception_and_EXIT(report=f"Current html text is an unexpected chapter. Expected Chapter: {chapter}. Actual Chapter: {split_text[0]}.\ntranslation: {translation}\ndriver.page_source\n{driver.page_source}")

                final_chapter_text = ""
                for verse in range(2, max_verse+1):
                    chapter_text = split_text[1]
                    split_text = [part.strip() for part in chapter_text.split(f"{verse}", 1)]
                    final_chapter_text += f"{split_text[0]}\n"
                final_chapter_text += split_text[1]

                with open(OUT_TXT, 'w', encoding='UTF-8') as file:
                    file.write(final_chapter_text)
            except:
                problem_chapters.append(ProblemChapter(translation, book, chapter, datetime.now()))

    driver.quit()
    TOR.stop()

    if problem_chapters:
        report = File(REPORTS_DIRECTORY, "problem_chapters", file=f"scrape_bible_book({Time.local_time_as_legal_filename()})")
        redirect_print_to_file(report, 'w', lambda: print_list(problem_chapters))

    return problem_chapters

def scrape_bible_txt(target_translations:list[str], offset_book_index = 0, start_chapter = 1):
    """
    * target_translations: supported length: 1-5
    * offset_book_index : (*optional*) - use when past partial scrapes have been done (1-65)
    """
    
    if offset_book_index != 0:
        assert_int("offset_book_index", offset_book_index, min_val=1, max_val=65)
    
    problem_chapters: list[ProblemChapter] = []
    for book in BIBLE.Books()[offset_book_index:]:
        problem_chapters.extend(scrape_bible_book(book, target_translations))
        print_green(f"{target_translations}:{book.name} Done.")
    
    report = File(REPORTS_DIRECTORY, "problem_chapters", file=Time.local_time_as_legal_filename())
    redirect_print_to_file(report, 'w', lambda: print_list(problem_chapters))