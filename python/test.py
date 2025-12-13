from datetime import datetime
import time
from definitions import *
from kozubenko.os import File, Parent
from kozubenko.print import Print
from models.Bible import BIBLE, Book
from scrape import ProblemChapter, Scrape, still_on_expected_path


def TEST_scrape_bible_book():
    # translations = ['KJV', 'NASB', 'RSV', 'NRSV', 'ESV']
    translations = ['ESV']
    book, chapter = BIBLE.random_chapter()

    with Scrape:
        Scrape.EnglishBook(translations, BIBLE.GENESIS, 49, 49)
        # Scrape.EnglishBook(translations, BIBLE.HOSEA, 9, 9)
        # Scrape.EnglishBook(translations, BIBLE.PSALMS, 12, 12)
        # Scrape.EnglishBook(translations, book, chapter, chapter)
        # book, chapter = BIBLE.random_chapter()
        # Scrape.EnglishBook(translations, book, chapter, chapter)
        # book, chapter = BIBLE.random_chapter()
        # Scrape.EnglishBook(translations, book, chapter, chapter)
        # book, chapter = BIBLE.random_chapter()
        # Scrape.EnglishBook(translations, book, chapter, chapter)
        # book, chapter = BIBLE.random_chapter()
        # Scrape.EnglishBook(translations, book, chapter, chapter)
        # book, chapter = BIBLE.random_chapter()
        # Scrape.EnglishBook(translations, book, chapter, chapter)
        # book, chapter = BIBLE.random_chapter()
        # Scrape.EnglishBook(translations, book, chapter, chapter)
        # book, chapter = BIBLE.random_chapter()
        # Scrape.EnglishBook(translations, book, chapter, chapter)


TEST_scrape_bible_book()