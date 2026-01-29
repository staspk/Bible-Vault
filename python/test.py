from parser import *
from models.bible_chapter_sets.missing_chapters import MissingChapters
from kozubenko.print import Print
from models.Bible import BIBLE
from models.BibleChapterSets import BibleChapterSets
from definitions import ALL_TRANSLATIONS
from transform import standardize_verse_form


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


# Chapters:BibleChapterSets = BibleChapterSets(identify_Standard_Form().marked)
# for chapter in Chapters.iterate():
#     iterate_verses(chapter)

# Print.red(Chapters.total)




standardize_verse_form()



"""
"{verse} \n" -> Lined Verse

"{verse} 

"{1 } \n{2 }" -> Standard Line

TODO: 
    to identify mixed form
    assert 1 Lined Verse
"""