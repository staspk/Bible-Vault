from collections.abc import KeysView
from dataclasses import dataclass, field
from operator import itemgetter
from kozubenko.cls import set_frozen_attr
from kozubenko.os import File
from kozubenko.parse import is_AlphaNumeric
from kozubenko.print import Print, colored_input
from kozubenko.string import List
from models.Bible import BIBLE as _BIBLE, Book, Iterate_Bible_Chapters
from models.BibleChapterSets import BibleChapterSets
from models.IChapter import IChapter
from models.bible_chapter_sets.abnormal_verse_count import abnormal_verse_count_Chapters
from models.bible_chapter_sets.missing_chapters import MissingChapters
from parser import load_verses
from tests.data.chapters import Test_Chapters
import definitions
from kozubenko import script



DIRECTORY = definitions.BIBLE_TXT_NEW
ALL_TRANSLATIONS = definitions.ALL_TRANSLATIONS
def ALL_CHAPTERS() -> BibleChapterSets: return BibleChapterSets.From(ALL_TRANSLATIONS).Mark(lambda Chapter:chapter_File(Chapter).exists()).Marked

def chapter_File(PTR:IChapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def chapter_text(PTR:IChapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')




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


def assemble_Chapters():
    chapters = {}
    for i,book,chapter_num in Iterate_Bible_Chapters():
        for translation in ALL_TRANSLATIONS:
            PTR = Chapter(translation, book, chapter_num)
            chapters[PTR] = None
    return chapters

type char = str
type occurrences = int

class BIBLE:
    _chapters:dict[Chapter, None] = None # assemble_Chapters()

    _chars:dict[char, occurrences] = None
    _words:dict[str, occurrences] = None

    # def __init__(self):
        

    @classmethod
    def chapters(cls) -> KeysView[Chapter]:
        if cls._chapters is None: cls._chapters = assemble_Chapters()
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


def search_Bible(search:str, book:list[Book]):
    pass


if __name__ == "__main__":
    Print.Args()

    search:str        = script.Arg1(required=False) or "Angel of the Lord"
    domain:list[Book] = List.From(script.Arg2())

    Print.green(domain)

    Print.green(_BIBLE.ACTS.total_verses(-1))
