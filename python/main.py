from definitions import *
from kozubenko.tor import Tor
from scrape_bible import *
from models.Bible import *



Tor.start()

for i in range(1, 67):
    scrape_basic_html(Bible[i], target_translation='NASB')



# scrape_basic_html(Bible[BIBLE.DEUTERONOMY])

# scrape_rsv_html(Bible[BIBLE.GENESIS])

# selenium_scrape(Bible[BIBLE.GENESIS])

# soup_scrape(Bible[BIBLE.GENESIS], start_chapter=50)
