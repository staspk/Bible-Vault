from kozubenko.dict import Dict, increment_value
from models.Bible import BIBLE, Chapter
from parser import ALL_CHAPTERS, BIBLE_TXT_PARTIAL, BIBLE_TXT_POSTPONED, move_Chapters, open_Chapters, chapter_File, identify_Chapters_missing_verses, identify_missing_chapters, identify_Standard_Form
from kozubenko.print import Print, colored_input
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters
from scrape import ProblemChapter



# identify_missing_chapters().Save_Report('identify_missing_chapters')
# identify_Chapters_missing_verses().Save_Report('identify_Chapters_missing_verses')
# identify_Standard_Form().Save_Report('identify_Standard_Form')
# TEST_iterate_verses().Save_Report('TEST_iterate_verses')


# Chapters = standardize_verse_form()

standardize_verse_form(only_report=True)


