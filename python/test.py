import time
from definitions import BIBLE_TXT_TO_MOVE, TEMP_DIR
from kozubenko.iter import iterate_list
from kozubenko.os import File
from models.text_forms.missing_verses import MissingVerses
# from scrape import Scrape
from models.text_forms.scrape_fail import ScrapeFail
from parser import *
from kozubenko.print import ANSI, Print, colored_input
from kozubenko.subprocess import Subprocess
from models.Bible import BIBLE, Chapter, Iterate_Bible_Chapters
from models.BibleChapters import BibleChapters, BibleChapterSets
from models.text_forms.standard import StandardForm
from models.text_forms.titled import TitledTrait


ALL_TRANSLATIONS = ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT', 'NIV', 'NET']

def debug_chapter(translation='KJV', book=BIBLE.SECOND_CHRONICLES, chapter=2):
    PTR = Chapter(book, chapter, None, translation)
    chapter_File(PTR).open()
    debug_chapter(translation, book, chapter, is_standard_form)

def identify_Standard_Form() -> BibleChapterSets:
    Chapters:BibleChapterSets = BibleChapterSets.From(ALL_TRANSLATIONS)
    for PTR in Chapters.iterate():
        if is_standard_form(PTR, chapter_text(PTR)):
            Chapters.mark(PTR.translation, PTR.index)

    Print.red(Chapters.total_marked)
    Chapters.Save_Report('identify_standard_form()', 'Standard Form')
    return Chapters

def identify_Poetry_Form() -> BibleChapterSets:
    Chapters:BibleChapterSets = BibleChapterSets(StandardForm.Inverse())
    for PTR in Chapters.iterate():
        chapter_File(PTR).open()
        Print.yellow(str(PTR))
        if is_poetry_form(PTR, chapter_text(PTR)):
            Chapters.mark(PTR.translation, PTR.index)
        
        # colored_input("waiting...", ANSI.YELLOW)

    Print.red(Chapters.total_marked)
    # Chapters.Save_Report()
    return Chapters


# Chapters = identify_Poetry_Form()
# visual_test(Chapters.iterate_marked)


# Chapters:BibleChapterSets = BibleChapterSets(StandardForm.Inverse())
# visual_test(Chapters.iterate)


def identify_Mixed_Form() -> BibleChapterSets:
    Chapters:BibleChapterSets = BibleChapterSets(StandardForm.Inverse())
    for PTR in Chapters.iterate():
        chapter_File(PTR).open()
        Print.yellow(str(PTR))
        if has_standard_line(PTR):
            Chapters.mark(PTR.translation, PTR.index)

def identify_Chapters_missing_verses() -> BibleChapterSets:
    Chapters:BibleChapterSets = BibleChapterSets.From(ALL_TRANSLATIONS)
    for PTR in Chapters.iterate():
        if has_missing_verses(PTR):
            Chapters.mark(PTR.translation, PTR.index)
        
    Print.red(Chapters.total_marked)
    Chapters.Save_Report('Missing Verses')
    return Chapters


MISSING_VERSES = BibleChapterSets(MissingVerses.Chapters())

FUCKUPS = BibleChapterSets(ScrapeFail.Chapters())

successes = MISSING_VERSES.subtract(FUCKUPS)
for PTR in successes.iterate():
    if has_missing_verses(PTR):
        successes.mark(PTR.translation, PTR.index)
        chapter_File(PTR).delete()
successes.Save_Report('New To Move')
Print.red(successes.total)
Print.red(successes.total_marked)



# for PTR in successes.iterate_marked():
#     chapter_File(PTR).move(File(BIBLE_TXT_TO_MOVE, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt'))

