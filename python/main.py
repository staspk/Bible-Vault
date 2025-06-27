from definitions import *
from kozubenko.os import Directory, Parent, TestPath
from kozubenko.utils import ScriptArg_1, assert_path_exists
from models.Bible import BIBLE
from scrape import *

"""
Skip Psalms for now...
Issues also in Song of Solomon

skipped Psalms / Proverbs for ['ESV', 'NIV', 'NET', 'RUSV', 'NRT']

Judges:20 [NRSV] -> verses 22/23 transposed


"""

start_scrape_index = int(ScriptArg_1(1))


eng_translations  = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
russ_translations = ['RUSV', 'NRT']
current           = ['ESV', 'NIV', 'NET', 'RUSV', 'NRT']


scrape_bible_txt(current, start_scrape_index)      # offset: 22 == Isaiah

# scrape_bible_book(BIBLE.ISAIAH, current, startChapter=3)