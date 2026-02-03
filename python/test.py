from parser import chapter_File
from search import BIBLE, Test
from transform import standardize_verse_form
from kozubenko.print import Print, colored_input
from models.IChapter import IChapter
from models.Bible import BIBLE as _BIBLE
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

# identify_missing_chapters().Save_Report('identify_missing_chapters')
# identify_Chapters_missing_verses().Save_Report('identify_Chapters_missing_verses')
# identify_Standard_Form().Save_Report('identify_Standard_Form')
# TEST_iterate_verses().Save_Report('TEST_iterate_verses')


# Chapters = standardize_verse_form()

# standardize_verse_form(only_report=True)


BIBLE.Top_Words(1000)