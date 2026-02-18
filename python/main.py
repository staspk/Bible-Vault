from scrape import Scrape
from parser import identify_missing_chapters
from kozubenko.os import File
from kozubenko.print import Print
from models.Bible import Chapter
from models.BibleChapterSets import BibleChapterSets
from definitions import *


eng_translations  = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
rus_translations  = ['RUSV', 'NRT']

def chapter_File(PTR:Chapter): return File(Scrape.OUT_DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')


# Scrape.Bible_Random_Order(rus_translations)

