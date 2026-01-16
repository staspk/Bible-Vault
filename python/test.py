from definitions import BIBLE_TXT_NEW
from scrape import Scrape
from parser import file
from kozubenko.os import File
from kozubenko.subprocess import Subprocess
from kozubenko.print import Print
from models.Bible import BIBLE, ChapterPtr
from models.BibleChapters import BibleChapters, BibleChapterSets
from models.text_forms.standard import StandardForm
from models.text_forms.titled import TitledTrait


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

def visual_test(chapters:BibleChapters, files_per_iteration=50):
    iteration = 1
    for PTR in chapters.iterate():
        Subprocess.Notepad(file(PTR))
        iteration += 1
        if iteration == files_per_iteration:
            input()
            iteration = 1

translations = ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT', 'NIV', 'NET']

# Chapters = BibleChapterSets(StandardForm.remaining_chapters())
# for PTR in Chapters.iterate():
#     FILE = file(PTR)
#     if FILE.exists():
#         if is_titled(PTR, FILE.contents(encoding='UTF-8')):
#             Chapters.mark(PTR.translation, PTR.index)

# Chapters.Save_Report()


# visual_test(BibleChapterSets(StandardForm.Chapters()))

Chapters:BibleChapterSets = BibleChapterSets.From(translations)
for PTR in Chapters.iterate():
    if not file(PTR).exists():
        Chapters.mark(PTR.translation, PTR.index)

Chapters.Save_Report('identify_missing_chapters()', 'Missing Chapters')

for PTR in Chapters.iterate_marked():
    Print.red(str(PTR))