from datetime import datetime
import time
from definitions import *
from kozubenko.os import File, Parent
from kozubenko.print import Print
from models.Bible import BIBLE, Book
from scrape import ProblemChapter, Scrape, still_on_expected_path


def TEST_scrape_bible_book():
    translations = ['NASB', 'RSV']
    book, chapter = BIBLE.random_chapter()
    print(f'{book} {chapter}')

    with Scrape:
        Scrape.Book(translations, BIBLE.HOSEA, 9, 9)
        Scrape.Book(translations, BIBLE.PSALMS, 12, 12)
        Scrape.Book(translations, book, chapter, chapter)
        book, chapter = BIBLE.random_chapter()
        Scrape.Book(translations, book, chapter, chapter)
        book, chapter = BIBLE.random_chapter()
        Scrape.Book(translations, book, chapter, chapter)


Print.green(DEFINITIONS_PY)
# TEST_scrape_bible_book()