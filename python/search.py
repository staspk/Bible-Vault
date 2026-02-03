from collections.abc import KeysView
from dataclasses import dataclass, field
from operator import itemgetter
from kozubenko.cls import set_frozen_attr
from kozubenko.os import File
from kozubenko.print import Print
from models.Bible import BIBLE as _BIBLE, Book, Iterate_Bible_Chapters
from models.BibleChapterSets import BibleChapterSets
from models.IChapter import IChapter
from models.bible_chapter_sets.missing_chapters import MissingChapters
from tests.data.chapters import chapters
from definitions import ALL_TRANSLATIONS, BIBLE_TXT_NEW


DIRECTORY = BIBLE_TXT_NEW
def ALL_CHAPTERS() -> BibleChapterSets: return BibleChapterSets.Subtract(BibleChapterSets.From(ALL_TRANSLATIONS).set, MissingChapters.chapters())

def chapter_File(PTR:IChapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def chapter_text(PTR:IChapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')

def strip_title(PTR:IChapter) -> tuple[str, str]:
    """
    **Returns:**
        `(title, rest)`
            `title == ""`, if no title in text
    """
    TEXT = chapter_text(PTR)
    lines = TEXT.splitlines(keepends=True)

    if lines[0] == "1\n": return ("", TEXT)

    # Every title <= 2 lines. To be safe, working backwards from line 5 to find first verse...
    i = 4
    while i > -1:
        if lines[i] == "1\n":
            title = "".join(lines[:i])
            rest  = "".join(lines[i:])
            return (title, rest)
        i -= 1
    
    raise Exception(f'strip_title(): Encountered text aberration. "1\n" not found! Chapter: {str(PTR)}')

def load_verses(PTR:IChapter) -> dict[verse_num, verse_text] | None:
    if not chapter_File(PTR).exists():
        return None

    verses = {}
    title, TEXT = strip_title(PTR)

    verse_num = 1
    start = TEXT.find('1\n') + len('1\n')
    end   = TEXT.find('\n2', start)
    verse_text = TEXT[start:end]
    verses[1] = verse_text

    while end != -1:
        verse_num += 1
        start = TEXT.find(f'{verse_num}\n', end) + len(f'{verse_num}\n')
        end   = TEXT.find(f'\n{verse_num+1}', start)
        verse_text = TEXT[start:end]
        if end != -1:
            verses[verse_num] = verse_text

    verses[verse_num] = TEXT[start:len(TEXT) - 1]
    return verses

verse_num = int
verse_text = str

@dataclass(frozen=True)
class Chapter:
    translation:str
    book:Book
    chapter:int
    verses:dict[verse_num, verse_text] = field(default=None, compare=False, hash=False)

    def __post_init__(self):
        if self.verses is None:
            set_frozen_attr(self, "verses", load_verses(self))

occurrences = int

class BIBLE:
    _Chapters:dict[Chapter, None] = None

    @classmethod
    def Chapters(cls) -> KeysView[Chapter]:
        if cls._Chapters is None:
            cls._Chapters = {}

            for i,book,chapter_num in Iterate_Bible_Chapters():
                for translation in ALL_TRANSLATIONS:
                    PTR = Chapter(translation, book, chapter_num)
                    cls._Chapters[PTR] = None

        return cls._Chapters.keys()
    

    words:dict[str, occurrences] = {}

    @classmethod
    def Top_Words(cls, step=1000):
        if not cls._Analyze_Words_has_run:
            cls.Analyze_Words()

        i = 0
        for word,occurrences in cls.words.items():
            Print.yellow(f'{word} -> {occurrences}')
            i += 1

            if i % step == 0:
                input()


    _Analyze_Words_has_run = False
    @classmethod
    def Analyze_Words(cls) -> dict[str, occurrences]:
        if len(cls.words.keys()) > 0:
            return cls.words

        for Chapter in cls.Chapters():
            if Chapter.verses is None:
                continue

            for verse_num, verse_text in Chapter.verses.items():
                words = " ".join(verse_text.splitlines()).split(" ")
                
                for word in words:
                    if word in cls.words: cls.words[word] += 1
                    else:                 cls.words[word]  = 1

        sorted_words = sorted(cls.words.items(), key=itemgetter(1), reverse=True)
        cls.words = {}

        for word,occurrences in sorted_words:
            cls.words[word] = occurrences

        return cls.words



class Test:
    def load_verses() -> bool:
        Tests = {
            IChapter('NET', _BIBLE.PSALMS, 42)          : None,
            IChapter('NRT', _BIBLE.FIRST_CHRONICLES, 3) : None,
        }

        for chapter in Tests:
            ACTUAL_VERSES = list(chapters.get(chapter).iterate_verses())
            VERSES = list(load_verses(chapter).values())

            if len(ACTUAL_VERSES) != len(VERSES):
                Tests[chapter] = False
                continue

            for i in range(len(VERSES)):
                verse = VERSES[i]
                actual_verse = ACTUAL_VERSES[i]
                if verse != actual_verse:
                    Tests[chapter] = False
                    continue
            
            Tests[chapter] = True

        return all(Tests.values())

