import time
from collections.abc import Callable
from definitions import TEMP_DIR
from kozubenko.os import File
from scrape import Scrape
from parser import chapter_file, chapter_text, is_poetry_form, strip_title, is_numbered_wrong, debug_chapter, visual_test
from kozubenko.print import ANSI, Print, colored_input
from kozubenko.subprocess import Subprocess
from models.Bible import BIBLE, ChapterPtr, Iterate_Bible_Chapters
from models.BibleChapters import BibleChapters, BibleChapterSets
from models.text_forms.standard import StandardForm
from models.text_forms.titled import TitledTrait


ALL_TRANSLATIONS = ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT', 'NIV', 'NET']

Chapters:BibleChapterSets = BibleChapterSets(StandardForm.Inverse())
for PTR in Chapters.iterate():
    (title, text) = strip_title(chapter_text(PTR))
    # File(TEMP_DIR, 'new_text.txt').save(text, encoding='UTF-8').open()
    # input()
    if is_poetry_form(PTR, text):
        Chapters.mark(PTR.translation, PTR.index)


Print.red(Chapters.total_marked)
Chapters.Save_Report()
# visual_test(Chapters.iterate)

# translation = 'NKJV'; book = BIBLE.SECOND_SAMUEL; chapter = 13
# Subprocess.Notepad(file(ChapterPtr(book, chapter, None, translation)))
# debug_chapter(translation, book, chapter, is_titled)



    # visual_test(Chapters.iterate_marked)

# standardize_chapter_number_formatting()

# debug_chapter('NRSV', BIBLE.GENESIS, 35, is_numbered_wrong)
# debug_chapter('NET', BIBLE.PSALMS, 55, is_numbered_wrong)

# Chapters:BibleChapterSets = BibleChapterSets(TitledTrait.Chapters())
# visual_test(Chapters.iterate)

