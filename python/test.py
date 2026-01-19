from typing import Any
from kozubenko.time import Timer
from scrape import Scrape
from parser import *
from kozubenko.print import ANSI, Print, colored_input
from kozubenko.subprocess import Subprocess
from models.Bible import BIBLE, Iterate_Bible_Chapters
from models.BibleChapters import BibleChapters, BibleChapterSets
from models.text_forms.standard import StandardForm


def test_problem_chapters():
    with Scrape:
        translations = ['NASB', 'RSV', 'ESV']
        Scrape.Book(translations, BIBLE.MATTHEW, 17, 17)    # iteration: 23
        Scrape.Book(translations, BIBLE.MATTHEW, 18, 18)    # iteration: 13,14,14
        Scrape.Book(translations, BIBLE.MATTHEW, 23, 23)    # iteration: 16,15,15
        Scrape.Book(translations, BIBLE.MARK, 7, 7)         # iteration: 21,20,21
        Scrape.Book(translations, BIBLE.MARK, 9, 9)         # iteration: 48,51,50
        Scrape.Book(translations, BIBLE.MARK, 15, 15)       # iteration: 31,32,32
        Scrape.Book(translations, BIBLE.JOHN, 5, 5)         # iteration: 5
        Scrape.Book(translations, BIBLE.ACTS, 8, 8)         # iteration: 46,46,47
        Scrape.Book(translations, BIBLE.ACTS, 15, 15)       # iteration: 41,40,41
        Scrape.Book(translations, BIBLE.ACTS, 24, 24)       # iteration: 9,9,9
        Scrape.Book(translations, BIBLE.ACTS, 28, 28)       # iteration: 40,41,40
        Scrape.Book(translations, BIBLE.ROMANS, 16, 16)     # iteration: 26

        translations = ['RSV', 'ESV']
        Scrape.Book(translations, BIBLE.MATTHEW, 12, 12)      # iteration: 61
        Scrape.Book(translations, BIBLE.MARK, 11, 11)         # iteration: 30
        Scrape.Book(translations, BIBLE.LUKE, 23, 23)         # iteration: 20,19
        Scrape.Book(translations, BIBLE.LUKE, 17, 17)         # iteration: 39,41

        translations = ['RSV']
        Scrape.Book(translations, BIBLE.EXODUS, 22, 22)             # iteration: 3
        Scrape.Book(translations, BIBLE.SECOND_CHRONICLES, 20, 20)  # iteration: 27
        Scrape.Book(translations, BIBLE.MATTHEW, 21, 21)            # iteration: 59
        Scrape.Book(translations, BIBLE.LUKE, 22, 22)               # iteration: 50
        Scrape.Book(translations, BIBLE.LUKE, 24, 24)               # iteration: 13
        Scrape.Book(translations, BIBLE.JAMES, 1, 1)                # iteration: 11

def visual_test(iterator:Callable, files_per_iteration=50):
    """ **iterator:** `Chapters.iterate()` || `Chapters.iterate_marked()` """
    iteration = 1
    for PTR in iterator():
        Subprocess.Notepad(file(PTR))
        iteration += 1
        if iteration == files_per_iteration:
            colored_input(f'Press Enter to open another {files_per_iteration} chapters in Notepad++...', ANSI.YELLOW)
            iteration = 1

ALL_TRANSLATIONS = ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT', 'NIV', 'NET']

Chapters = BibleChapterSets(StandardForm.Inverse())
for PTR in Chapters.iterate():
    if is_titled(PTR, text(PTR)):
        Chapters.mark(PTR.translation, PTR.index)

Print.red(Chapters.total_marked)
Chapters.Save_Report()
# visual_test(Chapters.iterate_marked)

# translation = 'NKJV'; book = BIBLE.SECOND_SAMUEL; chapter = 13
# Subprocess.Notepad(file(ChapterPtr(book, chapter, None, translation)))
# debug_chapter(translation, book, chapter, is_titled)


def standardize_chapter_number_formatting():
    """
    **From:**  `f'1 '`  
    **To:** `f'{PTR.chapter} '`
    """
    Chapters:BibleChapterSets = BibleChapterSets.From(ALL_TRANSLATIONS)
    for PTR in Chapters.iterate():
        if is_numbered_wrong(PTR, text(PTR)):
            Chapters.mark(PTR.translation, PTR.index)

    Print.yellow(Chapters.total_marked)
    
    visual_test(Chapters.iterate_marked)

# standardize_chapter_number_formatting()

