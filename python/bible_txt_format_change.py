


import os
from kozubenko.os import Directory, File
from definitions import BIBLE_TXT, PROJECT_ROOT_DIRECTORY
from kozubenko.print import print_green, print_red
from models.Bible import BIBLE


BIBLE_TXT_ORIGINAL = Directory(BIBLE_TXT)
BIBLE_TXT_NEW      = Directory(PROJECT_ROOT_DIRECTORY, "bible_txt_new")

TODO = ["ESV", "KJV", "NASB", "NET", "NIV", "NKJV", "NRSV", "NRT", "RSV", "RUSV"]

total_chapters = 0
for translation in TODO:
    for i in range(1, 67):
        BOOK_DIR = os.path.join(BIBLE_TXT_ORIGINAL, translation, BIBLE.Book(i).name)
        if(os.path.exists(BOOK_DIR)):
            for chapter_file in os.listdir(BOOK_DIR):
                print_green(chapter_file)
                total_chapters += 1

print_red(f"total chapters: {total_chapters}")