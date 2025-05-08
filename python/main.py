from definitions import *
from html_parser import parse_simple_html
from scrape_bible import *
from models.Bible import *



eng_translations = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
russ_translations = ['RUSV', 'NRT']


# stealth_scrape_chapter(Bible[BIBLE.GENESIS], 1, russ_translations)

# stealth_scrape(Bible[BIBLE.GENESIS], 'KJV')
parse_simple_html(Bible[BIBLE.GENESIS], 'RSV', one_pass=True)
