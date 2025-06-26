from definitions import *
from kozubenko.os import Directory, Parent, TestPath
from kozubenko.utils import ScriptArg_1, assert_path_exists
from models.Bible import BIBLE
from scrape import *

"""
Skip Psalms for now...
Issues also in Song of Solomon

Judges:20 [NRSV] -> verses 22/23 transposed
"""

start_scrape_index = int(ScriptArg_1(1))

eng_translations = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
russ_translations = ['RUSV', 'NRT']


scrape_bible_txt(['ESV', 'NIV', 'NET', 'RUSV', 'NRT'], 19)      # offset: 19 == Proverbs

# scrape_bible_txt(['KJV', 'NKJV', 'RSV', 'NRSV', 'NASB'], start_scrape_index)        # passed through entire bible once (see problem_chapters in ./reports)

# scrape_bible_txt(['NIV', 'NET', 'ESV', 'NLT', 'CEV'])