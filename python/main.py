from scrape import Scrape
from parser import identify_missing_chapters
from kozubenko.os import File
from kozubenko.print import Print
from models.Bible import Chapter
from models.BibleChapterSets import BibleChapterSets
from definitions import *


eng_translations  = ['KJV', 'NKJV', 'NASB', 'ESV', 'RSV', 'NRSV', 'NIV', 'NET']
rus_translations  = ['RUSV', 'NRT']

# Scrape.Bible_Random_Order(rus_translations)


def chapter_File(PTR:Chapter): return File(Scrape.OUT_DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')

Missing:BibleChapterSets = BibleChapterSets(identify_missing_chapters().marked)
with Scrape:
    for PTR in Missing.iterate():
        if not chapter_File(PTR).exists():
            Scrape.Book([PTR.translation], PTR.book, PTR.chapter, PTR.chapter)

        if chapter_File(PTR).exists():
            Missing.mark(PTR)

Missing.Save_Report('missing_chapters_scraped')


Chapters:BibleChapterSets = BibleChapterSets(identify_missing_chapters().marked)
for PTR in Chapters.iterate():
    if chapter_File(PTR).exists():
        Chapters.mark(PTR)

Print.red(Chapters.ratio())

# for potential_chapter in Chapters