from definitions import *
from models.Bible import BIBLE
from scrape import Scrape

"""
Psalms, Song of Solomon

Judges:20 [NRSV] -> verses 22/23 transposed

Lamentations [NET] -> starts with: א (Alef)

Skipping Ezekiel at  : NIV, NRT - Expected drop_cap: 29. Actual Text: Judgment. While Scraping: ['ESV', 'NIV', 'NET', 'RUSV', 'NRT']
Skipping Zephaniah at: NIV      - Expected drop_cap: 2.  Actual Text: Judah.    While Scraping: ['ESV', 'NIV', 'NET', 'RUSV', 'NRT']

"""

eng_translations  = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
rus_translations  = ['RUSV', 'NRT']


translations = ['KJV', 'NASB', 'RSV', 'NKJV', 'NRSV']
eng_left = ['ESV','NIV','NET']
Scrape.Bible_Random_Order(eng_left)
