from models.Bible import BIBLE
from parser import chapter_File, identify_missing_chapters
from kozubenko.print import Print, colored_input
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters
from definitions import ALL_TRANSLATIONS
from scrape import ProblemChapter


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


# Print.red(identify_missing_chapters().total_marked)



