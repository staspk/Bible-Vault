import sys
from definitions import BIBLE_JSON
import json

import bible


with open(BIBLE_JSON, 'r', encoding='utf-8') as file:
    bible = json.load(file)

size_in_bytes = sys.getsizeof(bible)

# for len(bible.item)
# for book_abbr, book in bible.items():
#     print(book_abbr, )

print(bible[5])
print(size_in_bytes)

bible.books.GENSIS