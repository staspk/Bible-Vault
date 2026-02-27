from kozubenko.print import Print
from kozubenko.timer import Timer
from models.Bible import BIBLE, Chapter, Construct_Bible
from models.BibleChapterSets import BibleChapterSets
from models.IChapter import IChapter
from models.bible_chapter_sets.missing_chapters import MissingChapters
from parser import ALL_CHAPTERS, BIBLE_TXT, BIBLE_TXT_PARTIAL, chapter_File, open_Chapters


# Bible = Construct_Bible()


PTR = IChapter('RSV', BIBLE.GENESIS, 1)

print(f'{PTR}')