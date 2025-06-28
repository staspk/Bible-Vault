from dataclasses import dataclass
import os

from definitions import BIBLE_NUMERICAL_MAP
from kozubenko.utils import assert_class, assert_int, assert_path_exists

"""
abbreviations for apocrypha:
    Tob
    Jdt
    GkEsth
    Wis
    Sir
    Bar
    EpJer
    SgThr
    Sus
    Bel
    1Macc
    2Macc
    1Esd
    PrMan
    Ps151
    3Ma
    2Esd
    4Ma
"""

@dataclass
class Book:
    """
    * name : str -> *"Genesis"*
    * abbr : str -> *consistent with BibleGateway's abbreviations*
    * index : int -> *numerical appearance in the bible, 1-66*
    *  chapters : int -> *total  chapters, e.g: 50*
    """
    name: str
    abbr: str
    index: int
    chapters: int

    def __str__(self):
        return self.name


class BIBLE: 
    GENESIS              = Book(name="Genesis",             abbr="Gen",      index=1,     chapters=50)
    EXODUS               = Book(name="Exodus",              abbr="Exod",     index=2,     chapters=40)
    LEVITICUS            = Book(name="Leviticus",           abbr="Lev",      index=3,     chapters=27)
    NUMBERS              = Book(name="Numbers",             abbr="Num",      index=4,     chapters=36)
    DEUTERONOMY          = Book(name="Deuteronomy",         abbr="Deut",     index=5,     chapters=34)
    JOSHUA               = Book(name="Joshua",              abbr="Josh",     index=6,     chapters=24)
    JUDGES               = Book(name="Judges",              abbr="Judg",     index=7,     chapters=21)
    RUTH                 = Book(name="Ruth",                abbr="Ruth",     index=8,     chapters=4)
    FIRST_SAMUEL         = Book(name="1 Samuel",            abbr="1Sam",     index=9,     chapters=31)
    SECOND_SAMUEL        = Book(name="2 Samuel",            abbr="2Sam",     index=10,    chapters=24)
    FIRST_KINGS          = Book(name="1 Kings",             abbr="1Kgs",     index=11,    chapters=22)
    SECOND_KINGS         = Book(name="2 Kings",             abbr="2Kgs",     index=12,    chapters=25)
    FIRST_CHRONICLES     = Book(name="1 Chronicles",        abbr="1Chr",     index=13,    chapters=29)
    SECOND_CHRONICLES    = Book(name="2 Chronicles",        abbr="2Chr",     index=14,    chapters=36)
    EZRA                 = Book(name="Ezra",                abbr="Ezra",     index=15,    chapters=10)
    NEHEMIAH             = Book(name="Nehemiah",            abbr="Neh",      index=16,    chapters=13)
    ESTHER               = Book(name="Esther",              abbr="Esth",     index=17,    chapters=10)
    JOB                  = Book(name="Job",                 abbr="Job",      index=18,    chapters=42)
    PSALMS               = Book(name="Psalms",              abbr="Ps",       index=19,    chapters=150)
    PROVERBS             = Book(name="Proverbs",            abbr="Prov",     index=20,    chapters=31)
    ECCLESIASTES         = Book(name="Ecclesiastes",        abbr="Eccl",     index=21,    chapters=12)
    SONG_OF_SOLOMON      = Book(name="Song of Solomon",     abbr="Song",     index=22,    chapters=8)
    ISAIAH               = Book(name="Isaiah",              abbr="Isa",      index=23,    chapters=66)
    JEREMIAH             = Book(name="Jeremiah",            abbr="Jer",      index=24,    chapters=52)
    LAMENTATIONS         = Book(name="Lamentations",        abbr="Lam",      index=25,    chapters=5)
    EZEKIEL              = Book(name="Ezekiel",             abbr="Ezek",     index=26,    chapters=48)
    DANIEL               = Book(name="Daniel",              abbr="Dan",      index=27,    chapters=12)
    HOSEA                = Book(name="Hosea",               abbr="Hos",      index=28,    chapters=14)
    JOEL                 = Book(name="Joel",                abbr="Joel",     index=29,    chapters=3)
    AMOS                 = Book(name="Amos",                abbr="Amos",     index=30,    chapters=9)
    OBADIAH              = Book(name="Obadiah",             abbr="Obad",     index=31,    chapters=1)
    JONAH                = Book(name="Jonah",               abbr="Jonah",    index=32,    chapters=4)
    MICAH                = Book(name="Micah",               abbr="Mic",      index=33,    chapters=7)
    NAHUM                = Book(name="Nahum",               abbr="Nah",      index=34,    chapters=3)
    HABAKKUK             = Book(name="Habakkuk",            abbr="Hab",      index=35,    chapters=3)
    ZEPHANIAH            = Book(name="Zephaniah",           abbr="Zeph",     index=36,    chapters=3)
    HAGGAI               = Book(name="Haggai",              abbr="Hag",      index=37,    chapters=2)
    ZECHARIAH            = Book(name="Zechariah",           abbr="Zech",     index=38,    chapters=14)
    MALACHI              = Book(name="Malachi",             abbr="Mal",      index=39,    chapters=4)
    MATTHEW              = Book(name="Matthew",             abbr="Matt",     index=40,    chapters=28)
    MARK                 = Book(name="Mark",                abbr="Mark",     index=41,    chapters=16)
    LUKE                 = Book(name="Luke",                abbr="Luke",     index=42,    chapters=24)
    JOHN                 = Book(name="John",                abbr="John",     index=43,    chapters=21)
    ACTS                 = Book(name="Acts",                abbr="Acts",     index=44,    chapters=28)
    ROMANS               = Book(name="Romans",              abbr="Rom",      index=45,    chapters=16)
    FIRST_CORINTHIANS    = Book(name="1 Corinthians",       abbr="1Cor",     index=46,    chapters=16)
    SECOND_CORINTHIANS   = Book(name="2 Corinthians",       abbr="2Cor",     index=47,    chapters=13)
    GALATIANS            = Book(name="Galatians",           abbr="Gal",      index=48,    chapters=6)
    EPHESIANS            = Book(name="Ephesians",           abbr="Eph",      index=49,    chapters=6)
    PHILIPPIANS          = Book(name="Philippians",         abbr="Phil",     index=50,    chapters=4)
    COLOSSIANS           = Book(name="Colossians",          abbr="Col",      index=51,    chapters=4)
    FIRST_THESSALONIANS  = Book(name="1 Thessalonians",     abbr="1Thess",   index=52,    chapters=5)
    SECOND_THESSALONIANS = Book(name="2 Thessalonians",     abbr="2Thess",   index=53,    chapters=3)
    FIRST_TIMOTHY        = Book(name="1 Timothy",           abbr="1Tim",     index=54,    chapters=6)
    SECOND_TIMOTHY       = Book(name="2 Timothy",           abbr="2Tim",     index=55,    chapters=4)
    TITUS                = Book(name="Titus",               abbr="Titus",    index=56,    chapters=3)
    PHILEMON             = Book(name="Philemon",            abbr="Phlm",     index=57,    chapters=1)
    HEBREWS              = Book(name="Hebrews",             abbr="Heb",      index=58,    chapters=13)
    JAMES                = Book(name="James",               abbr="Jas",      index=59,    chapters=5)
    FIRST_PETER          = Book(name="1 Peter",             abbr="1Pet",     index=60,    chapters=5)
    SECOND_PETER         = Book(name="2 Peter",             abbr="2Pet",     index=61,    chapters=3)
    FIRST_JOHN           = Book(name="1 John",              abbr="1John",    index=62,    chapters=5)
    SECOND_JOHN          = Book(name="2 John",              abbr="2John",    index=63,    chapters=1)
    THIRD_JOHN           = Book(name="3 John",              abbr="3John",    index=64,    chapters=1)
    JUDE                 = Book(name="Jude",                abbr="Jude",     index=65,    chapters=1)
    REVELATION           = Book(name="Revelation",          abbr="Rev",      index=66,    chapters=22)

    _Books:list[Book] = None        # Lazy-loaded. Use BIBLE.Books() to access

    def Book(index:int) -> Book:
        """
        returns a Book by index (not by offset), i.e: `BIBLE.Book(1) -> Genesis`
        """
        assert_int("index", index, 1, 66)
        return BIBLE.Books()[index - 1]

    def Books() -> list[Book]:
        """
        returns the standard 66 books as a list[Book].
        """
        if BIBLE._Books is None:
            BIBLE._Books = []
            for name, book in BIBLE.__dict__.items():
                if not name.startswith("__") and isinstance(book, Book):
                    BIBLE._Books.append(book)

        return BIBLE._Books        

    def find_max_verse(book:Book, chapter:int) -> int:
        assert_class("book", book, Book)
        assert_int("chapter", chapter, 1, book. chapters)

        path = os.path.join(BIBLE_NUMERICAL_MAP, str(book.index))
        assert_path_exists("path", path)
        
        with open(path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file, start=1):
                if(i == chapter):
                    return int(line.split(':')[2])
        
        raise Exception("Bible.py:find_max_verse(): unreachable code path reached. BIBLE_NUMERICAL_MAP is broken!")