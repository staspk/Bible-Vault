from definitions import *
from kozubenko.os import Directory, Parent, TestPath
from kozubenko.utils import ScriptArg_1, assert_path_exists
from models.Bible import BIBLE
from html_parser import *
from scrape import *

"""
Skip Psalms for now...
Issues also in Song of Solomon
"""

start_scrape_index = int(ScriptArg_1(22))

eng_translations = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
russ_translations = ['RUSV', 'NRT']

scrape_bible_txt(['KJV', 'NKJV', 'RSV', 'NRSV', 'NASB'], start_scrape_index)
# scrape_bible_txt(['NIV', 'NET', 'ESV', 'NLT', 'CEV'])