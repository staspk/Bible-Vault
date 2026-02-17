from parser import chapter_File
from kozubenko.print import colored_input
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters
from definitions import ALL_TRANSLATIONS


def ALL_CHAPTERS() -> BibleChapterSets: return BibleChapterSets.Subtract(BibleChapterSets.From(ALL_TRANSLATIONS).set, MissingChapters.chapters())

# identify_missing_chapters().Save_Report('identify_missing_chapters')
# identify_Chapters_missing_verses().Save_Report('identify_Chapters_missing_verses')
# identify_Standard_Form().Save_Report('identify_Standard_Form')


Chapters:BibleChapterSets = MissingChapters.Chapters()
Chapters.Mark(lambda Chapter:Chapter.translation == 'NRT')






# Print.green(Chapter(BIBLE.JOSHUA, 5, 'NRT').total_verses)