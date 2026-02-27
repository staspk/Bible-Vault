from kozubenko.print import Print
from kozubenko.timer import Timer
from models.Bible import BIBLE, Chapter, Construct_Bible
from models.BibleChapterSets import BibleChapterSets
from models.IChapter import IChapter
from models.bible_chapter_sets.missing_chapters import MissingChapters
from parser import ALL_CHAPTERS, BIBLE_TXT, BIBLE_TXT_PARTIAL, Test, chapter_File, open_Chapters, load_verses_FOR_abnormal_verse_count_Chapter


# Bible = Construct_Bible()


# PTR = IChapter('RSV', BIBLE.EXODUS, 22)
# chapter_File(BIBLE_TXT, PTR).open()
# load_verses_FOR_abnormal_verse_count_Chapter(PTR)

Test.load_verses()