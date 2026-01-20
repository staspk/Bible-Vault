import time
from collections.abc import Callable
from definitions import TEMP_DIR
from kozubenko.os import File
from scrape import Scrape
from parser import chapter_File, chapter_text, has_standard_line, is_poetry_form, is_standard_form, strip_title, is_numbered_wrong, debug_chapter, visual_test
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

def identify_Standard_Form() -> BibleChapters:
    Chapters:BibleChapterSets = BibleChapterSets.From(ALL_TRANSLATIONS)
    for PTR in Chapters.iterate():
        if is_standard_form(PTR, chapter_text(PTR)):
            Chapters.mark(PTR.translation, PTR.index)

    Print.red(Chapters.total_marked)
    Chapters.Save_Report('identify_standard_form()', 'Standard Form')
    return Chapters

def identify_Poetry_Form() -> BibleChapters:
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


def identify_Mixed_Form() -> BibleChapters:
    Chapters:BibleChapterSets = BibleChapterSets(StandardForm.Inverse())
    for PTR in Chapters.iterate():
        chapter_File(PTR).open()
        Print.yellow(str(PTR))
        if has_standard_line(PTR):
            Chapters.mark(PTR.translation, PTR.index)

# identify_Mixed_Form()

chapter = Chapter(BIBLE.JOHN, 1)
Print.green(str(chapter))