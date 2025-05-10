from definitions import *
from models.Bible import BIBLE
from html_parser import *
from scrape import *


eng_translations = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
russ_translations = ['RUSV', 'NRT']


# stealth_scrape_chapter(Bible[BIBLE.GENESIS], 1, russ_translations)


stealth_scrape(BIBLE.GENESIS, 'KJV')
parse_simple_html(BIBLE.GENESIS, 'KJV', one_pass=False)

