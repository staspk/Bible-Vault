import random
from parser import *
from transform import compare_changes, standardize_verse_form
from kozubenko.print import Print, colored_input
from models.Bible import BIBLE
from models.BibleChapterSets import BibleChapterSets, Protestant_Set
from models.bible_chapter_sets.missing_chapters import MissingChapters
from definitions import ALL_TRANSLATIONS, BIBLE_TXT


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


# Print.green(standardize_verse_form().total_marked)
# standardize_verse_form(BibleChapterSets({
#     'NRSV':{788}
# }))

def chapter_File(PTR:Chapter): return File(BIBLE_TXT, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def chapter_text(PTR:Chapter): return File(BIBLE_TXT, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')

books = [BIBLE.FIRST_KINGS, BIBLE.FIRST_CHRONICLES, BIBLE.SECOND_CHRONICLES, BIBLE.SECOND_KINGS, BIBLE.SECOND_SAMUEL, BIBLE.ECCLESIASTES, BIBLE.ESTHER, BIBLE.EZRA, BIBLE.JOB, BIBLE.NEHEMIAH, BIBLE.PROVERBS, BIBLE.PSALMS, BIBLE.SONG_OF_SOLOMON, BIBLE.ZEPHANIAH]
for book in books:
    for chapter in range(1, book.chapters+1):
        PTR = Chapter(book, chapter, translation='RUSV')
        TEXT = chapter_text(PTR)
        new_text = ""

        lines = TEXT.splitlines()
        for verse_num, verse in enumerate(lines, start=1):
            new_text += f"{verse[len(str(verse_num))+1:]}\n"

        chapter_File(PTR).save(new_text)


# Chapters = BibleChapterSets.Subtract(BibleChapterSets({'RUSV':Protestant_Set()}).set, MissingChapters.chapters())
# for PTR in Chapters.iterate():
#     if is_standard_form(PTR):
#         Chapters.mark(PTR)
# Print.yellow(Chapters.total_marked)

"""
"{verse} \n" -> Lined Verse

"{verse} 

"{1 } \n{2 }" -> Standard Line

TODO: 
    to identify mixed form
    assert 1 Lined Verse
"""