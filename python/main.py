from definitions import *
from kozubenko.cls import class_attributes
from kozubenko.os import Directory
from kozubenko.subprocess import Subprocess
from models.Bible import BIBLE
from models.BibleChapters import BibleChapterSets, Protestant_Set
from models.text_forms.missing_verses import MissingVerses
from parser import chapter_File
from scrape import Book, Scrape


eng_translations  = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
rus_translations  = ['RUSV', 'NRT']

# Scrape.Bible_Random_Order(rus_translations)


with Scrape(BIBLE_TXT_PARTIAL):
    Scrape.ChapterSet(MissingVerses.iterate)