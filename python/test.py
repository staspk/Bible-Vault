from kozubenko.print import Print
from models.Bible import BIBLE, construct_Bible
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters


Chapters:BibleChapterSets = MissingChapters.Chapters()


Bible = construct_Bible()

# Print.yellow(Bible['RSV'][BIBLE.GENESIS][1][1])

bible = {}


