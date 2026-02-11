from models.Bible import BIBLE
from parser import chapter_File, identify_missing_chapters
from kozubenko.print import Print, colored_input
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters
from definitions import ALL_TRANSLATIONS
from scrape import ProblemChapter


def ALL_CHAPTERS() -> BibleChapterSets: return BibleChapterSets.Subtract(BibleChapterSets.From(ALL_TRANSLATIONS).set, MissingChapters.chapters())



# identify_missing_chapters().Save_Report('identify_missing_chapters')
# identify_Chapters_missing_verses().Save_Report('identify_Chapters_missing_verses')
# identify_Standard_Form().Save_Report('identify_Standard_Form')
# TEST_iterate_verses().Save_Report('TEST_iterate_verses')


# Print.red(identify_missing_chapters().total_marked)



open_Chapters(ALL_CHAPTERS())