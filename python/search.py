from collections.abc import KeysView
from dataclasses import dataclass, field
from operator import itemgetter
from kozubenko.cls import set_frozen_attr
from kozubenko.os import File
from kozubenko.parse import is_AlphaNumeric
from kozubenko.print import Print, colored_input
from kozubenko.script import Script
from models.Bible import BIBLE as _BIBLE, Book, Iterate_Bible_Chapters
from models.BibleChapterSets import BibleChapterSets
from models.IChapter import IChapter
from models.bible_chapter_sets.abnormal_verse_count import abnormal_verse_count_Chapters
from models.bible_chapter_sets.missing_chapters import MissingChapters
from tests.data.chapters import chapters
import definitions


DIRECTORY = definitions.BIBLE_TXT_NEW
ALL_TRANSLATIONS = definitions.ALL_TRANSLATIONS
def ALL_CHAPTERS() -> BibleChapterSets: return BibleChapterSets.From(ALL_TRANSLATIONS).Mark(lambda Chapter:chapter_File(Chapter).exists()).Marked

def chapter_File(PTR:IChapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def chapter_text(PTR:IChapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')


type title = str; type rest = str
def strip_title(PTR:IChapter) -> tuple[title, rest]:
    """
    `title == ""`, if no `title` in Chapter text
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

    def find_verse_text(verse_num:int, start:int, end:int) -> tuple[int, int]:
        start = TEXT.find(f'{verse_num}\n', end) + len(f'{verse_num}\n')
        end   = TEXT.find(f'\n{verse_num+1}', start)
        if end != -1:
            verses[verse_num] = TEXT[start:end]
            verse_num += 1

        return verse_num, start, end

    
    verse_num, start, end = find_verse_text(1, 0, len(TEXT))
    while end != -1:
        verse_num, start, end = find_verse_text(verse_num, start, end)

    verses[verse_num] = TEXT[start:len(TEXT) - 1]   # last verse

    return verses

type verse_num = int
type verse_text = str

@dataclass(frozen=True)
class Chapter:
    translation:str
    book:Book
    chapter:int
    verses:dict[verse_num, verse_text] = field(default=None, compare=False, hash=False)

    def __post_init__(self):
        set_frozen_attr(self, "index", _BIBLE.find_chapter_index(self.book, self.chapter))

        if self.verses is None and not abnormal_verse_count_Chapters.includes(self):
            set_frozen_attr(self, "verses", load_verses(self))


def load_chapters():
    chapters = {}
    for i,book,chapter_num in Iterate_Bible_Chapters():
        for translation in ALL_TRANSLATIONS:
            PTR = Chapter(translation, book, chapter_num)
            chapters[PTR] = None
    return chapters

type char = str
type occurrences = int

class BIBLE:
    _chapters:dict[Chapter, None] = load_chapters()

    _chars:dict[char, occurrences] = None
    _words:dict[str, occurrences] = None

    # def __init__(self):
        

    @classmethod
    def chapters(cls) -> KeysView[Chapter]:
        if cls._chapters is None: cls._chapters = load_chapters()
        return cls._chapters.keys()

    @classmethod
    def analyze_chars(cls) -> dict[char, occurrences]:
        if cls._chars:
            return cls._chars
        
        cls._chars = {}
        for Chapter in cls.chapters():
            if Chapter.verses is None:
                continue

            for verse_text in Chapter.verses.values():
                words = " ".join(verse_text.splitlines()).split(" ")

                for char in words:
                    for char in char:
                        if char in cls._chars: cls._chars[char] += 1
                        else:                  cls._chars[char]  = 1
        
        sorted_chars = sorted(cls._chars.items(), key=itemgetter(1), reverse=True)
        cls._chars = {}
        for char,occurrences in sorted_chars:
            cls._chars[char] = occurrences

        return cls._chars

    @classmethod
    def analyze_words(cls) -> dict[str, occurrences]:
        if cls._words:
            return cls._words
        
        cls._words = {}
        for Chapter in cls.chapters():
            if Chapter.verses is None:
                continue

            for verse_text in Chapter.verses.values():
                words = " ".join(verse_text.splitlines()).split(" ")
                
                for word in words:
                    if word in cls._words: cls._words[word] += 1
                    else:                  cls._words[word]  = 1

        sorted_words = sorted(cls._words.items(), key=itemgetter(1), reverse=True)
        cls._words = {}
        for word,occurrences in sorted_words:
            cls._words[word] = occurrences

        return cls._words

    @classmethod
    def Top_Words(cls, step=1000):
        if cls._words is None:
            cls.analyze_words()

        i = 0
        for word,occurrences in cls._words.items():
            # if not is_AlphaNumeric(word):
            Print.yellow(f'{word} -> {occurrences}')
            i += 1

            if i % step == 0:
                colored_input(f'Press Enter for {step} more...')

    @classmethod
    def Top_Chars(cls):
        if cls._chars is None:
            cls.analyze_chars()

        for char,occurrences in cls._chars.items():
            if not char.isalnum():
                Print.yellow(f'{char} -> {occurrences}')


if __name__ == "__main__":
    search:str = Script.Arg1()



    




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

