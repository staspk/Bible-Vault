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
    name     : str -> "Genesis"
    abbr     : str -> consistent with BibleGateway's abbreviations
    chapters : int -> total chapters, e.g: 50
    index    : int -> numerical appearance in the bible, 1-66
    """
    name: str
    abbr: str
    chapters: int
    index: int

    def __str__(self):
        return self.name


class BIBLE: 
    GENESIS              = Book(name='Genesis',             abbr='Gen',      chapters=50,    index=1)
    EXODUS               = Book(name='Exodus',              abbr='Exod',     chapters=40,    index=2)
    LEVITICUS            = Book(name='Leviticus',           abbr='Lev',      chapters=27,    index=3)
    NUMBERS              = Book(name='Numbers',             abbr='Num',      chapters=36,    index=4)
    DEUTERONOMY          = Book(name='Deuteronomy',         abbr='Deut',     chapters=34,    index=5)
    JOSHUA               = Book(name='Joshua',              abbr='Josh',     chapters=24,    index=6)
    JUDGES               = Book(name='Judges',              abbr='Judg',     chapters=21,    index=7)
    RUTH                 = Book(name='Ruth',                abbr='Ruth',     chapters=4,     index=8)
    FIRST_SAMUEL         = Book(name='1 Samuel',            abbr='1Sam',     chapters=31,    index=9)
    SECOND_SAMUEL        = Book(name='2 Samuel',            abbr='2Sam',     chapters=24,    index=10)
    FIRST_KINGS          = Book(name='1 Kings',             abbr='1Kgs',     chapters=22,    index=11)
    SECOND_KINGS         = Book(name='2 Kings',             abbr='2Kgs',     chapters=25,    index=12)
    FIRST_CHRONICLES     = Book(name='1 Chronicles',        abbr='1Chr',     chapters=29,    index=13)
    SECOND_CHRONICLES    = Book(name='2 Chronicles',        abbr='2Chr',     chapters=36,    index=14)
    EZRA                 = Book(name='Ezra',                abbr='Ezra',     chapters=10,    index=15)
    NEHEMIAH             = Book(name='Nehemiah',            abbr='Neh',      chapters=13,    index=16)
    ESTHER               = Book(name='Esther',              abbr='Esth',     chapters=10,    index=17)
    JOB                  = Book(name='Job',                 abbr='Job',      chapters=42,    index=18)
    PSALMS               = Book(name='Psalms',              abbr='Ps',       chapters=150,   index=19)
    PROVERBS             = Book(name='Proverbs',            abbr='Prov',     chapters=31,    index=20)
    ECCLESIASTES         = Book(name='Ecclesiastes',        abbr='Eccl',     chapters=12,    index=21)
    SONG_OF_SOLOMON      = Book(name='Song of Solomon',     abbr='Song',     chapters=8,     index=22)
    ISAIAH               = Book(name='Isaiah',              abbr='Isa',      chapters=66,    index=23)
    JEREMIAH             = Book(name='Jeremiah',            abbr='Jer',      chapters=52,    index=24)
    LAMENTATIONS         = Book(name='Lamentations',        abbr='Lam',      chapters=5,     index=25)
    EZEKIEL              = Book(name='Ezekiel',             abbr='Ezek',     chapters=48,    index=26)
    DANIEL               = Book(name='Daniel',              abbr='Dan',      chapters=12,    index=27)
    HOSEA                = Book(name='Hosea',               abbr='Hos',      chapters=14,    index=28)
    JOEL                 = Book(name='Joel',                abbr='Joel',     chapters=3,     index=29)
    AMOS                 = Book(name='Amos',                abbr='Amos',     chapters=9,     index=30)
    OBADIAH              = Book(name='Obadiah',             abbr='Obad',     chapters=1,     index=31)
    JONAH                = Book(name='Jonah',               abbr='Jonah',    chapters=4,     index=32)
    MICAH                = Book(name='Micah',               abbr='Mic',      chapters=7,     index=33)
    NAHUM                = Book(name='Nahum',               abbr='Nah',      chapters=3,     index=34)
    HABAKKUK             = Book(name='Habakkuk',            abbr='Hab',      chapters=3,     index=35)
    ZEPHANIAH            = Book(name='Zephaniah',           abbr='Zeph',     chapters=3,     index=36)
    HAGGAI               = Book(name='Haggai',              abbr='Hag',      chapters=2,     index=37)
    ZECHARIAH            = Book(name='Zechariah',           abbr='Zech',     chapters=14,    index=38)
    MALACHI              = Book(name='Malachi',             abbr='Mal',      chapters=4,     index=39)
    MATTHEW              = Book(name='Matthew',             abbr='Matt',     chapters=28,    index=40)
    MARK                 = Book(name='Mark',                abbr='Mark',     chapters=16,    index=41)
    LUKE                 = Book(name='Luke',                abbr='Luke',     chapters=24,    index=42)
    JOHN                 = Book(name='John',                abbr='John',     chapters=21,    index=43)
    ACTS                 = Book(name='Acts',                abbr='Acts',     chapters=28,    index=44)
    ROMANS               = Book(name='Romans',              abbr='Rom',      chapters=16,    index=45)
    FIRST_CORINTHIANS    = Book(name='1 Corinthians',       abbr='1Cor',     chapters=16,    index=46)
    SECOND_CORINTHIANS   = Book(name='2 Corinthians',       abbr='2Cor',     chapters=13,    index=47)
    GALATIANS            = Book(name='Galatians',           abbr='Gal',      chapters=6,     index=48)
    EPHESIANS            = Book(name='Ephesians',           abbr='Eph',      chapters=6,     index=49)
    PHILIPPIANS          = Book(name='Philippians',         abbr='Phil',     chapters=4,     index=50)
    COLOSSIANS           = Book(name='Colossians',          abbr='Col',      chapters=4,     index=51)
    FIRST_THESSALONIANS  = Book(name='1 Thessalonians',     abbr='1Thess',   chapters=5,     index=52)
    SECOND_THESSALONIANS = Book(name='2 Thessalonians',     abbr='2Thess',   chapters=3,     index=53)
    FIRST_TIMOTHY        = Book(name='1 Timothy',           abbr='1Tim',     chapters=6,     index=54)
    SECOND_TIMOTHY       = Book(name='2 Timothy',           abbr='2Tim',     chapters=4,     index=55)
    TITUS                = Book(name='Titus',               abbr='Titus',    chapters=3,     index=56)
    PHILEMON             = Book(name='Philemon',            abbr='Phlm',     chapters=1,     index=57)
    HEBREWS              = Book(name='Hebrews',             abbr='Heb',      chapters=13,    index=58)
    JAMES                = Book(name='James',               abbr='Jas',      chapters=5,     index=59)
    FIRST_PETER          = Book(name='1 Peter',             abbr='1Pet',     chapters=5,     index=60)
    SECOND_PETER         = Book(name='2 Peter',             abbr='2Pet',     chapters=3,     index=61)
    FIRST_JOHN           = Book(name='1 John',              abbr='1John',    chapters=5,     index=62)
    SECOND_JOHN          = Book(name='2 John',              abbr='2John',    chapters=1,     index=63)
    THIRD_JOHN           = Book(name='3 John',              abbr='3John',    chapters=1,     index=64)
    JUDE                 = Book(name='Jude',                abbr='Jude',     chapters=1,     index=65)
    REVELATION           = Book(name='Revelation',          abbr='Rev',      chapters=22,    index=66)

    def book_list() -> list[Book]:
        list:Book = []
        for name, book in BIBLE.__dict__.items():
            if not name.startswith('__') and isinstance(book, Book):
                list.append(book)
        return list

    def find_max_verse(book:Book, chapter:int) -> int:
        assert_class("book", book, Book)
        assert_int("chapter", chapter, 1, book.chapters)

        path = os.path.join(BIBLE_NUMERICAL_MAP, str(book.index))
        assert_path_exists("path", path)
        
        with open(path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file, start=1):
                if(i == chapter):
                    return int(line.split(':')[2])
        
        raise Exception('Bible.py:find_max_verse(): unreachable code path reached. BIBLE_NUMERICAL_MAP is broken!')