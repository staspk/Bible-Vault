import time, random
from typing import Any, Iterator, Self
from dataclasses import dataclass, fields
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from definitions import *
from tor.tor import Tor
from kozubenko.print import *
from kozubenko.os import File
from kozubenko.iter import iterate_list
from kozubenko.string import String
from kozubenko.utils import assert_bool, assert_class, assert_int, assert_list
from models.Bible import BIBLE, Book, Chapter
from models.BibleChapterSets import BibleChapterSets
from models.IChapter import IChapter



@dataclass
class ProblemChapter:
    translation:str
    book:Book
    chapter:int
    reason:str=""
    dt=datetime.now().strftime("%Y/%m/%d %H:%M")

    def __str__(self) -> str:
        return (
            f"Problem Chapter: {self.book.name} {self.chapter} [{self.translation}]\n"
            f"Found At: {str(self.dt)}\n"
            f"Reason: {self.reason}"
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
    ```python
    page_options = DriverInstructionsToFindMe(driver)
    page_options.set_states()
    ```
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
    
    def AttemptToSetPageState(
        driver:RemoteWebDriver,
        cross_references:bool=None, footnotes:bool=None, verse_numbers:bool=None, headings:bool=None, red_letter:bool=None
    ) -> bool:
        try:
            page_options = BibleGatewayOptions.DriverInstructionsToFindMe(driver)
            page_options.set_states(cross_references, footnotes, verse_numbers, headings, red_letter)
            return True
        except:
            try:
                time.sleep(.075)
                page_options = BibleGatewayOptions.DriverInstructionsToFindMe(driver)
                time.sleep(.125)
                page_options.set_states(cross_references, footnotes, verse_numbers, headings, red_letter)
                return True
            except:
                try:
                    time.sleep(.1)
                    page_options = BibleGatewayOptions.DriverInstructionsToFindMe(driver)
                    time.sleep(.2)
                    page_options.set_states(cross_references, footnotes, verse_numbers, headings, red_letter)
                    return True
                except:
                    return False

    @classmethod
    def DriverInstructionsToFindMe(cls, driver:RemoteWebDriver) -> Self:
        cls.settings_icon = WebDriverWait(driver, 10).until(                                # operation time avg: ~15ms
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.settings"))
        )
        time.sleep(1.25)
        cls.settings_icon.click()

        settings_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".bg-tooltip.options-tooltip"))
        )
        page_options_checkboxes = settings_div.find_elements(By.CSS_SELECTOR, "div[style*='cursor: pointer;'] svg")
        page_options_toggles    = settings_div.find_elements(By.CSS_SELECTOR, "div[style*='cursor: pointer;']")
        page_options_states     = [True if svg.get_attribute("name") == "checked" else False for svg in page_options_checkboxes]
        page_options_states_and_toggles = [BibleGatewayOption(state, toggle) for state, toggle in zip(page_options_states, page_options_toggles)]
        page_options                    = cls(*page_options_states_and_toggles)

        return page_options
    
    def set_states(self, cross_references:bool=None, footnotes:bool=None, verse_numbers:bool=None, headings:bool=None, red_letter:bool=None):
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

def still_on_expected_path(expected_cls:str, actual_cls:str) -> str|False:
    """
    Assumption/expectation as we iterate through BibleGateway `spans` holding verse-line/verse,  
    is that these spans will iterate the verse_number in it's class, i.e:
       
    **If** current_verse -> Hosea 9:3  
    `cls` can only ever be:  
    `text Hos-9-3` OR `text Hos-9-4`

    **If** we encounter anything else, continuing will yield a corrupted text/chapter

    **Returns:** `expected_cls`, iterated `expected_cls`, OR `False`
    """
    if expected_cls != actual_cls:
        rest, verse = expected_cls.rsplit('-', 1)
        verse = int(verse)
        verse += 1
        new_cls = f'{rest}-{verse}'
        if new_cls != actual_cls:
            return False   # 'expected_cls is neither actual_cls, nor actual_cls+1'
        return new_cls
    else:
        return expected_cls

class ScrapeContextManager(type):
    def __enter__(cls):
        if Scrape.OUT_DIRECTORY is None: raise Exception('Must Set: Scrape.OUT_DIRECTORY')
        Tor.Start()
        Scrape.setup_driver()
        return cls

    def __exit__(cls, exc_type, exc_val, exc_tb):
        if(Scrape.driver): Scrape.driver.quit()
        Tor.Stop()

class Scrape(metaclass=ScrapeContextManager):
    OUT_DIRECTORY:str = BIBLE_TXT_PARTIAL # BIBLE_TXT_NEW
    driver:Any = None

    problem_chapters:list[ProblemChapter] = []

    def handle(problem:ProblemChapter):
        Scrape.problem_chapters.append(problem)
        Print.yellow(f'{str(problem)}\n')

    def setup_driver():
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type",             1)
        profile.set_preference("network.proxy.socks",            Tor.HOST)
        profile.set_preference("network.proxy.socks_port",       Tor.socks_port)
        profile.set_preference("network.proxy.socks_remote_dns", True)
        profile.set_preference("browser.cache.disk.enable",      False)
        profile.set_preference("browser.cache.memory.enable",    False)

        options = Options()
        options.profile = profile
        # options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)
        Scrape.driver = driver


    chapter_text = str

    def parse_chapter(translation:str, book:Book, chapter:int) -> chapter_text | None:
        css_selector_for_chapter = f"[class*='version-{translation}'][class*='result-text-style-normal'][class*='text-html']"
        element = Scrape.driver.find_element(By.CSS_SELECTOR, css_selector_for_chapter)

        selector = f"span[class*='text {book.abbr}-{chapter}-']"
        spans:list[WebElement] = element.find_elements(By.CSS_SELECTOR, selector)

        expected_cls = f"text {book.abbr}-{chapter}-1"
        chapter_text = ""
        iteration = 0
    
        for span in spans:
            iteration += 1

            debug1 = Test.still_on_expected_path_about_to_return_False(expected_cls, span.get_attribute("class"))

            # expected_cls = still_on_expected_path(expected_cls, span.get_attribute("class"))
            # if expected_cls == False:
            #     Scrape.handle(ProblemChapter(translation, book, chapter, f'not still_on_expected_path() on iteration: {iteration}')) 
            #     return None

            if String.isEmptyOrWhitespace(span.text):
                continue

            chapter_text += f"{span.text}\n"

        return chapter_text

    def Book(target_translations:list[str], book:Book, startChapter = 1, lastChapter:int=None):
        """
        - `target_translations` -> len(1-5)

        **EXAMPLE:**
        ```python
        with Scrape:
            Scrape.Book(translations, book, chapter, chapter)
            Scrape.Book(translations, book, chapter, chapter)
        ```
        """
        assert_class("book", book, Book)
        assert_list("target_translations", target_translations, min_len=1, max_len=5)
        assert_int("startChapter", startChapter, min_val=1, max_val=book.chapters)
        if lastChapter is None:
            lastChapter = book.chapters
        assert_int("lastChapter", lastChapter, min_val=1, max_val=book.chapters)

        for chapter in range(startChapter, lastChapter+1):
            URL = fr"https://www.biblegateway.com/passage/?search={book.abbr}%20{chapter}&version={";".join(target_translations)}"

            Scrape.driver.get(URL)

            if not BibleGatewayOptions.AttemptToSetPageState(Scrape.driver, False, False, True, False, True):
                Scrape.handle(ProblemChapter(None, book, chapter, 'AttemptToSetPageState() failure'))
                continue

            for translation in target_translations:
                OUT_TXT = File(Scrape.OUT_DIRECTORY, translation, book.name, f'{chapter}.txt')

                chapter_text = Scrape.parse_chapter(translation, book, chapter)
                if chapter_text:
                    OUT_TXT.save(chapter_text, encoding='UTF-8')

    def Bible(target_translations:list[str], index_book_start = 1, index_book_end = 66):
        """
        - `target_translations` - supported length: 1-5

        Relies on: `Scrape.Book()`
        """
        assert_int("index_book_start", index_book_start, min_val=1,                max_val=66)
        assert_int("index_book_end",   index_book_end,   min_val=index_book_start, max_val=66)
        
        for book in BIBLE.Books()[index_book_start-1:index_book_end]:
            Scrape.Book(book, target_translations)
            Print.green(f"{target_translations}:{book.name} Done.")

    def Bible_Random_Order(target_translations:list[str], out_dir:str=None):
        """
        NOTE: Written before `BibleChapters`/`BibleChapterSets` existed. Plug in, if you ever use this again.

        Relies on: `Scrape.Book()`
        """
        if out_dir is None:
            out_dir = Scrape.OUT_DIRECTORY

        def chapter_already_scraped(chapter:int) -> bool:
            PTR:Chapter = BIBLE.Chapter(chapter)
            for translation in target_translations:
                if File(out_dir, translation, PTR.book.name, f'{PTR.chapter}.txt').exists():
                    return True
            return False

        chapters_todo = set(range(1, 1190))
        requests = 0; MAX_REQUESTS_PER_IP = 5
        with Scrape:
            while chapters_todo.__len__() > 0:
                chapter:int = random.choice(tuple(chapters_todo))
                if chapter_already_scraped(chapter):
                    chapters_todo.remove(chapter)
                    continue

                PTR:Chapter = BIBLE.Chapter(chapter)
                Scrape.Book(target_translations, PTR.book, PTR.chapter, PTR.chapter)
                Print.green(f'{PTR.book} {PTR.chapter}')
                chapters_todo.remove(chapter)

                requests += 1
                if requests > MAX_REQUESTS_PER_IP:
                    requests = 0
                    Tor.RotateIP()
                    Scrape.driver = None
                    Scrape.setup_driver()


    translation = str

    def scrape_chapter(translation:str, Chapter:IChapter) -> bool:
        """ Don't let the name confuse you - this is only a helper to `Scrape.ChapterSet` """
        OUT_TXT = File(Scrape.OUT_DIRECTORY, translation, Chapter.book.name, f'{Chapter.chapter}.txt')

        css_selector_for_chapter = f"[class*='version-{translation}'][class*='result-text-style-normal'][class*='text-html']"
        element = Scrape.driver.find_element(By.CSS_SELECTOR, css_selector_for_chapter)

        selector = f"span[class*='text {Chapter.book.abbr}-{Chapter.chapter}-']"
        spans:list[WebElement] = element.find_elements(By.CSS_SELECTOR, selector)

        expected_cls = f"text {Chapter.book.abbr}-{Chapter.chapter}-1"
        chapter_text = ""
        iteration = 0
        for span in spans:
            iteration += 1
            expected_cls = still_on_expected_path(expected_cls, span.get_attribute("class"))
            if expected_cls == False:
                return False
            if String.isEmptyOrWhitespace(span.text):
                continue

            chapter_text += f"{span.text}\n"

        OUT_TXT.save(chapter_text, encoding='UTF-8')
        return True

    def ChapterSet(Chapter_iterator:Callable[[], Iterator[tuple[Chapter, list[translation]]]]) -> BibleChapterSets:
        """
        **Returns:** `Chapters` unable to scrape.

        **EXAMPLE:**:
        ```python
        with Scrape:
            Scrape.ChapterSet(MissingChapters.iterate)
        ```
        """
        Chapters = BibleChapterSets({})
        for CHAPTER,TRANSLATIONS, in Chapter_iterator():
            for translations in iterate_list(TRANSLATIONS, step=5):
                if len(translations) > 1:
                    URL = fr"https://www.biblegateway.com/passage/?search={CHAPTER.book.abbr}%20{CHAPTER.chapter}&version={";".join(translations)}"

                    Scrape.driver.get(URL)

                    if not BibleGatewayOptions.AttemptToSetPageState(Scrape.driver, False, False, True, False, True):
                        for translation in translations:
                            Chapters.mark(Chapter.From(CHAPTER.index, translation=translation))
                        continue

                    for translation in translations:
                        if not Scrape.scrape_chapter(translation, CHAPTER):
                            Chapters.mark(Chapter.From(CHAPTER.index, translation=translation))

        return BibleChapterSets(Chapters.marked)


class Test:
    def IP_Rotations():
        with Scrape:
            for i in range(100):
                Scrape.driver.get('https://api.ipify.org')
                IP = Scrape.driver.find_element("tag name", "pre").text.strip()
                Print.green(f'IP: {IP}')
                Scrape.driver = None
                time.sleep(5)
                Tor.RotateIP()
                Scrape.setup_driver()

    def still_on_expected_path_about_to_return_False(expected_cls:str, actual_cls:str) -> str|False:
        return not still_on_expected_path(expected_cls, actual_cls)
