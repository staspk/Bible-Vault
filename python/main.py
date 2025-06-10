from definitions import *
from kozubenko.os import Directory, Parent, TestPath
from kozubenko.utils import AssertPathExists
from models.Bible import BIBLE
from html_parser import *
from scrape import *


eng_translations = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
russ_translations = ['RUSV', 'NRT']


# stealth_scrape_chapter(BIBLE.GENESIS, 1, russ_translations)

# scrape_bible_text(BIBLE.GENESIS, ['KJV', 'nkjv', 'esv', 'NASB', 'rsv'])
scrape_bible_text(BIBLE.GENESIS, ['ESV', 'NASB'])

# stealth_scrape_one(BIBLE.DANIEL, eng_translations, 1)
# parse_html(BIBLE.DANIEL, 'NASB', True)




# def load_into_memory(path:str):
#     AssertPathExists("path", path)
    
    
# main = Parent(Parent(__file__)) + r'\bible_txt\\RSV-v1'

# load_into_memory(main)