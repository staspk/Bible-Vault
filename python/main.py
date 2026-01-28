from definitions import *
from models.bible_chapter_sets.missing_chapters import MissingChapters
from scrape import Scrape
from kozubenko.print import Print


eng_translations  = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
rus_translations  = ['RUSV', 'NRT']

# Scrape.Bible_Random_Order(rus_translations)

with Scrape:
    Scrape.ChapterSet(MissingChapters.iterate) 
