from parser import *
from kozubenko.print import Print
from models.Bible import BIBLE
from models.IBibleChapterSet import IBibleChapterSet
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.standard import StandardForm
from models.bible_chapter_sets.missing_verses import MissingVerses
from models.bible_chapter_sets.missing_chapters import MissingChapters
from models.bible_chapter_sets.chapters_failing_iterate_verses import IterateVersesFails


ALL_TRANSLATIONS = ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT', 'NIV', 'NET']
ALL_CHAPTERS:BibleChapterSets = BibleChapterSets.Subtract(BibleChapterSets.From(ALL_TRANSLATIONS).set, MissingChapters.chapters())

def open_Chapters(Chapters:BibleChapterSets, step=50):
    i = 0
    for Chapter in Chapters.iterate():
        chapter_File(Chapter).open()
        i += 1
        if i == 50:
            colored_input(f'Press Enter for {step} more...')
            i = 0

# Chapters:BibleChapterSets = identify_Standard_Form()
# for chapter in Chapters.iterate():
#     continue

identify_missing_chapters()
identify_Chapters_missing_verses()
identify_Standard_Form()
TEST_iterate_verses()




"""
"{verse} \n" -> Lined Verse

"{verse} 

"{1 } \n{2 }" -> Standard Line

TODO: 
    to identify mixed form
    assert 1 Lined Verse
"""