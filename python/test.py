from kozubenko.print import Print
from models.Bible import BIBLE, Chapter, Construct_Bible
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters
from parser import ALL_CHAPTERS, chapter_File, BIBLE_TXT


Chapters:BibleChapterSets = MissingChapters.Chapters()


Bible = Construct_Bible()
