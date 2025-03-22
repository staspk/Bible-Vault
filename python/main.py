from datetime import datetime
import json as JSON
from definitions import *
from kozubenko.io import load_json
from python.kozubenko.time import Timer
from scrape_bible import *
from models.Bible import *



dt = datetime.utcnow()

print(dt)

# for i in range(1, 67):
    # print_yellow(Bible[i])
    # scrape_basic_html(Bible[i], target_translation='NASB')

# json = load_json('rsv.json')

# for data in json['data']:
#     print_yellow(data['chapter'])


# pass

# scrape_basic_html(Bible[BIBLE.DEUTERONOMY])

# scrape_rsv_html(Bible[BIBLE.GENESIS])

# selenium_scrape(Bible[BIBLE.GENESIS])

# soup_scrape(Bible[BIBLE.GENESIS], start_chapter=50)



# for book in Bible.values():
#     if book.index > 4:
#         print_yellow(book)
    # scrape_basic_html(Bible[BIBLE.DEUTERONOMY])

# print(Bible[BIBLE.GENESIS])

