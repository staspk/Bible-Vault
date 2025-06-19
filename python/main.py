from definitions import *
from kozubenko.os import Directory, Parent, TestPath
from kozubenko.utils import assert_path_exists
from models.Bible import BIBLE
from html_parser import *
from scrape import *


eng_translations = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
russ_translations = ['RUSV', 'NRT']


scrape_bible_txt(['KJV', 'NKJV', 'RSV', 'NRSV', 'NASB'])