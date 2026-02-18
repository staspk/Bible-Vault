from parser import BIBLE_TXT, BIBLE_TXT_PARTIAL, BIBLE_TXT_CURRENT, BIBLE_TXT_POSTPONED, open_Chapters, chapter_File
from kozubenko.print import Print, colored_input
from models.Bible import BIBLE, Chapter
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters
from models.bible_chapter_sets.abnormal_verse_count import Chapters_abnormal_verse_count
from definitions import ALL_TRANSLATIONS
from transform import standardize_verse_form_FOR_abnormal_verse_count


def ALL_CHAPTERS() -> BibleChapterSets: return BibleChapterSets.Subtract(BibleChapterSets.From(ALL_TRANSLATIONS).set, MissingChapters.chapters())

# identify_missing_chapters().Save_Report('identify_missing_chapters')
# identify_Chapters_missing_verses().Save_Report('identify_Chapters_missing_verses')
# identify_Standard_Form().Save_Report('identify_Standard_Form')


# Chapters:BibleChapterSets = MissingChapters.Chapters()
# Chapters.Mark(lambda Chapter:Chapter.translation == 'NRT')

standardize_verse_form_FOR_abnormal_verse_count(BIBLE_TXT_PARTIAL, only_report=True)