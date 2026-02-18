from parser import ALL_CHAPTERS, BIBLE_TXT, BIBLE_TXT_PARTIAL, BIBLE_TXT_CURRENT, BIBLE_TXT_POSTPONED, identify_missing_chapters, move_Chapters, open_Chapters, chapter_File
from kozubenko.print import Print, colored_input
from models.Bible import BIBLE, Chapter
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters
from models.bible_chapter_sets.abnormal_verse_count import abnormal_verse_count_Chapters
from definitions import ALL_TRANSLATIONS, BIBLE_TXT_NEW
from transform import standardize_verse_form_FOR_abnormal_verse_count
import search


# Chapters:BibleChapterSets = MissingChapters.Chapters()
# Chapters.Mark(lambda Chapter:Chapter.translation == 'NRT')

# standardize_verse_form_FOR_abnormal_verse_count(BIBLE_TXT_PARTIAL, only_report=False)
# open_Chapters(BIBLE_TXT_PARTIAL, Chapters_abnormal_verse_count.Chapters())

search.BIBLE.analyze_words()