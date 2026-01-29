from parser import *
from transform import standardize_verse_form
from kozubenko.print import Print, colored_input
from models.Bible import BIBLE
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters
from definitions import ALL_TRANSLATIONS


def ALL_CHAPTERS() -> BibleChapterSets: return BibleChapterSets.Subtract(BibleChapterSets.From(ALL_TRANSLATIONS).set, MissingChapters.chapters())

def open_Chapters(Chapters:BibleChapterSets, step=50):
    i = 0
    for Chapter in Chapters.iterate():
        chapter_File(Chapter).open()
        i += 1
        if i == 50:
            colored_input(f'Press Enter for {step} more...')
            i = 0

# Chapters:BibleChapterSets = BibleChapterSets(identify_Standard_Form().marked)
# for chapter in Chapters.iterate():
#     continue


standardize_verse_form(Chapter(BIBLE.GENESIS, 46, translation='NKJV'))




"""
"{verse} \n" -> Lined Verse

"{verse} 

"{1 } \n{2 }" -> Standard Line

TODO: 
    to identify mixed form
    assert 1 Lined Verse
"""