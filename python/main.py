from definitions import *
from kozubenko.os import Directory, Parent, TestPath
from kozubenko.utils import ScriptArg_1
from models.Bible import BIBLE
from scrape import *

"""
Psalms, Song of Solomon

Judges:20 [NRSV] -> verses 22/23 transposed

Lamentations [NET] -> starts with: א (Alef)

Skipping Ezekiel at  : NIV, NRT - Expected drop_cap: 29. Actual Text: Judgment. While Scraping: ['ESV', 'NIV', 'NET', 'RUSV', 'NRT']
Skipping Zephaniah at: NIV      - Expected drop_cap: 2.  Actual Text: Judah.    While Scraping: ['ESV', 'NIV', 'NET', 'RUSV', 'NRT']

"""

# scrape_bible_book(BIBLE.EZEKIEL, ['ESV', 'NET', 'RUSV'], 29)
# exit(0)

start_scrape_index = int(ScriptArg_1())

Print.yellow(f'{start_scrape_index}: {BIBLE.Book(start_scrape_index)}')

eng_translations  = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
rus_translations = ['RUSV', 'NRT']
current           = ['ESV', 'NIV', 'NET', 'RUSV', 'NRT']                            # ESV;NIV;NET;RUSV;NRT


scrape_bible_txt(current, start_scrape_index)      # offset: 33 == Micah