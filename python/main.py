import json as JSON
from definitions import *
from kozubenko.io import load_json
from kozubenko.timer import Timer
from kozubenko.utils import *
from scrape_bible import *
from models.Bible import *


# scrape_basic_html(Bible[BIBLE.DEUTERONOMY])

# scrape_rsv_html(Bible[BIBLE.GENESIS])

# selenium_scrape(Bible[BIBLE.GENESIS])

soup_scrape(Bible[BIBLE.GENESIS], start_chapter=50)



# for book in Bible.values():
#     if book.index > 4:
#         print_yellow(book)
    # scrape_basic_html(Bible[BIBLE.DEUTERONOMY])

# print(Bible[BIBLE.GENESIS])

# for i in range(4, 66):
#     scrape_basic_html(Bible[i])