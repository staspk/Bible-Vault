from definitions import *
from kozubenko.os import Directory, Parent, TestPath
from models.Bible import BIBLE
from html_parser import *
from scrape import *


eng_translations = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
russ_translations = ['RUSV', 'NRT']


# stealth_scrape_chapter(BIBLE.GENESIS, 1, russ_translations)

scrape_bible(BIBLE.GENESIS, ['KJV', 'NASB', 'RSV', 'RUSV'])

# stealth_scrape_one(BIBLE.DANIEL, eng_translations, 1)
# parse_html(BIBLE.DANIEL, 'NASB', True)







# def load_into_memory(path:str):
#     if not os.path.exists(path):
#         raise Exception(f'path does not exist: {path}')
    
#     for book in BIBLE.book_list():
#        print_cyan(book.name)

# main = Parent(Parent(__file__)) + r'\bible_txt\\RSV-v1'

# load_into_memory(main)