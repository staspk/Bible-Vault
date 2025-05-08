from dataclasses import dataclass
from enum import IntEnum
import os

from definitions import BIBLE_NUMERICAL_MAP

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
    Value in: `Bible:dict[BIBLE, Book]`\n
    name     : str -> "Genesis"
    abbr     : str -> consistent with BibleGateway's abbreviations
    chapters : int -> total chapters, e.g: 50
    index    : int -> numerical appearance in the bible, 1-66
    """
    name: str
    abbr: str
    chapters: int
    index: int


class BIBLE(IntEnum):
    """
    Key in: `Bible:dict[BIBLE, Book]`
    """
    GENESIS               =  1
    EXODUS                =  2
    LEVITICUS             =  3
    NUMBERS               =  4
    DEUTERONOMY           =  5
    JOSHUA                =  6
    JUDGES                =  7
    RUTH                  =  8
    FIRST_SAMUEL          =  9
    SECOND_SAMUEL         =  10
    FIRST_KINGS           =  11
    SECOND_KINGS          =  12
    FIRST_CHRONICLES      =  13
    SECOND_CHRONICLES     =  14
    EZRA                  =  15
    NEHEMIAH              =  16
    ESTHER                =  17
    JOB                   =  18
    PSALMS                =  19
    PROVERBS              =  20
    ECCLESIASTES          =  21
    SONG_OF_SOLOMON       =  22
    ISAIAH                =  23
    JEREMIAH              =  24
    LAMENTATIONS          =  25
    EZEKIEL               =  26
    DANIEL                =  27
    HOSEA                 =  28
    JOEL                  =  29
    AMOS                  =  30
    OBADIAH               =  31
    JONAH                 =  32
    MICAH                 =  33
    NAHUM                 =  34
    HABAKKUK              =  35
    ZEPHANIAH             =  36
    HAGGAI                =  37
    ZECHARIAH             =  38
    MALACHI               =  39
    MATTHEW               =  40
    MARK                  =  41
    LUKE                  =  42
    JOHN                  =  43
    ACTS                  =  44
    ROMANS                =  45
    FIRST_CORINTHIANS     =  46
    SECOND_CORINTHIANS    =  47
    GALATIANS             =  48
    EPHESIANS             =  49
    PHILIPPIANS           =  50
    COLOSSIANS            =  51
    FIRST_THESSALONIANS   =  52
    SECOND_THESSALONIANS  =  53
    FIRST_TIMOTHY         =  54
    SECOND_TIMOTHY        =  55
    TITUS                 =  56
    PHILEMON              =  57
    HEBREWS               =  58
    JAMES                 =  59
    FIRST_PETER           =  60
    SECOND_PETER          =  61
    FIRST_JOHN            =  62
    SECOND_JOHN           =  63
    THIRD_JOHN            =  64
    JUDE                  =  65
    REVELATION            =  66


Bible: dict[BIBLE, Book] = {
    BIBLE.GENESIS:               Book(name='Genesis',                   abbr='Gen',      chapters=50,    index=1),
    BIBLE.EXODUS:                Book(name='Exodus',                    abbr='Exod',     chapters=40,    index=2),
    BIBLE.LEVITICUS:             Book(name='Leviticus',                 abbr='Lev',      chapters=27,    index=3),
    BIBLE.NUMBERS:               Book(name='Numbers',                   abbr='Num',      chapters=36,    index=4),
    BIBLE.DEUTERONOMY:           Book(name='Deuteronomy',               abbr='Deut',     chapters=34,    index=5),
    BIBLE.JOSHUA:                Book(name='Joshua',                    abbr='Josh',     chapters=24,    index=6),
    BIBLE.JUDGES:                Book(name='Judges',                    abbr='Judg',     chapters=21,    index=7),
    BIBLE.RUTH:                  Book(name='Ruth',                      abbr='Ruth',     chapters=4,     index=8),
    BIBLE.FIRST_SAMUEL:          Book(name='1 Samuel',                  abbr='1Sam',     chapters=31,    index=9),
    BIBLE.SECOND_SAMUEL:         Book(name='2 Samuel',                  abbr='2Sam',     chapters=24,    index=10),
    BIBLE.FIRST_KINGS:           Book(name='1 Kings',                   abbr='1Kgs',     chapters=22,    index=11),
    BIBLE.SECOND_KINGS:          Book(name='2 Kings',                   abbr='2Kgs',     chapters=25,    index=12),
    BIBLE.FIRST_CHRONICLES:      Book(name='1 Chronicles',              abbr='1Chr',     chapters=29,    index=13),
    BIBLE.SECOND_CHRONICLES:     Book(name='2 Chronicles',              abbr='2Chr',     chapters=36,    index=14),
    BIBLE.EZRA:                  Book(name='Ezra',                      abbr='Ezra',     chapters=10,    index=15),
    BIBLE.NEHEMIAH:              Book(name='Nehemiah',                  abbr='Neh',      chapters=13,    index=16),
    BIBLE.ESTHER:                Book(name='Esther',                    abbr='Esth',     chapters=10,    index=17),
    BIBLE.JOB:                   Book(name='Job',                       abbr='Job',      chapters=42,    index=18),
    BIBLE.PSALMS:                Book(name='Psalms',                    abbr='Ps',       chapters=150,   index=19),
    BIBLE.PROVERBS:              Book(name='Proverbs',                  abbr='Prov',     chapters=31,    index=20),
    BIBLE.ECCLESIASTES:          Book(name='Ecclesiastes',              abbr='Eccl',     chapters=12,    index=21),
    BIBLE.SONG_OF_SOLOMON:       Book(name='Song of Solomon',           abbr='Song',     chapters=8,     index=22),
    BIBLE.ISAIAH:                Book(name='Isaiah',                    abbr='Isa',      chapters=66,    index=23),
    BIBLE.JEREMIAH:              Book(name='Jeremiah',                  abbr='Jer',      chapters=52,    index=24),
    BIBLE.LAMENTATIONS:          Book(name='Lamentations',              abbr='Lam',      chapters=5,     index=25),
    BIBLE.EZEKIEL:               Book(name='Ezekiel',                   abbr='Ezek',     chapters=48,    index=26),
    BIBLE.DANIEL:                Book(name='Daniel',                    abbr='Dan',      chapters=12,    index=27),
    BIBLE.HOSEA:                 Book(name='Hosea',                     abbr='Hos',      chapters=14,    index=28),
    BIBLE.JOEL:                  Book(name='Joel',                      abbr='Joel',     chapters=3,     index=29),
    BIBLE.AMOS:                  Book(name='Amos',                      abbr='Amos',     chapters=9,     index=30),
    BIBLE.OBADIAH:               Book(name='Obadiah',                   abbr='Obad',     chapters=1,     index=31),
    BIBLE.JONAH:                 Book(name='Jonah',                     abbr='Jonah',    chapters=4,     index=32),
    BIBLE.MICAH:                 Book(name='Micah',                     abbr='Mic',      chapters=7,     index=33),
    BIBLE.NAHUM:                 Book(name='Nahum',                     abbr='Nah',      chapters=3,     index=34),
    BIBLE.HABAKKUK:              Book(name='Habakkuk',                  abbr='Hab',      chapters=3,     index=35),
    BIBLE.ZEPHANIAH:             Book(name='Zephaniah',                 abbr='Zeph',     chapters=3,     index=36),
    BIBLE.HAGGAI:                Book(name='Haggai',                    abbr='Hag',      chapters=2,     index=37),
    BIBLE.ZECHARIAH:             Book(name='Zechariah',                 abbr='Zech',     chapters=14,    index=38),
    BIBLE.MALACHI:               Book(name='Malachi',                   abbr='Mal',      chapters=4,     index=39),
    BIBLE.MATTHEW:               Book(name='Matthew',                   abbr='Matt',     chapters=28,    index=40),
    BIBLE.MARK:                  Book(name='Mark',                      abbr='Mark',     chapters=16,    index=41),
    BIBLE.LUKE:                  Book(name='Luke',                      abbr='Luke',     chapters=24,    index=42),
    BIBLE.JOHN:                  Book(name='John',                      abbr='John',     chapters=21,    index=43),
    BIBLE.ACTS:                  Book(name='Acts',                      abbr='Acts',     chapters=28,    index=44),
    BIBLE.ROMANS:                Book(name='Romans',                    abbr='Rom',      chapters=16,    index=45),
    BIBLE.FIRST_CORINTHIANS:     Book(name='1 Corinthians',             abbr='1Cor',     chapters=16,    index=46),
    BIBLE.SECOND_CORINTHIANS:    Book(name='2 Corinthians',             abbr='2Cor',     chapters=13,    index=47),
    BIBLE.GALATIANS:             Book(name='Galatians',                 abbr='Gal',      chapters=6,     index=48),
    BIBLE.EPHESIANS:             Book(name='Ephesians',                 abbr='Eph',      chapters=6,     index=49),
    BIBLE.PHILIPPIANS:           Book(name='Philippians',               abbr='Phil',     chapters=4,     index=50),
    BIBLE.COLOSSIANS:            Book(name='Colossians',                abbr='Col',      chapters=4,     index=51),
    BIBLE.FIRST_THESSALONIANS:   Book(name='1 Thessalonians',           abbr='1Thess',   chapters=5,     index=52),
    BIBLE.SECOND_THESSALONIANS:  Book(name='2 Thessalonians',           abbr='2Thess',   chapters=3,     index=53),
    BIBLE.FIRST_TIMOTHY:         Book(name='1 Timothy',                 abbr='1Tim',     chapters=6,     index=54),
    BIBLE.SECOND_TIMOTHY:        Book(name='2 Timothy',                 abbr='2Tim',     chapters=4,     index=55),
    BIBLE.TITUS:                 Book(name='Titus',                     abbr='Titus',    chapters=3,     index=56),
    BIBLE.PHILEMON:              Book(name='Philemon',                  abbr='Phlm',     chapters=1,     index=57),
    BIBLE.HEBREWS:               Book(name='Hebrews',                   abbr='Heb',      chapters=13,    index=58),
    BIBLE.JAMES:                 Book(name='James',                     abbr='Jas',      chapters=5,     index=59),
    BIBLE.FIRST_PETER:           Book(name='1 Peter',                   abbr='1Pet',     chapters=5,     index=60),
    BIBLE.SECOND_PETER:          Book(name='2 Peter',                   abbr='2Pet',     chapters=3,     index=61),
    BIBLE.FIRST_JOHN:            Book(name='1 John',                    abbr='1John',    chapters=5,     index=62),
    BIBLE.SECOND_JOHN:           Book(name='2 John',                    abbr='2John',    chapters=1,     index=63),
    BIBLE.THIRD_JOHN:            Book(name='3 John',                    abbr='3John',    chapters=1,     index=64),
    BIBLE.JUDE:                  Book(name='Jude',                      abbr='Jude',     chapters=1,     index=65),
    BIBLE.REVELATION:            Book(name='Revelation',                abbr='Rev',      chapters=22,    index=66)
}


def find_max_verse(book:BIBLE, chapter:int) -> int:
    if not isinstance(book, BIBLE):
        raise Exception('Bible.py:find_max_verse(): book must be of IntEnum:Book')

    if(0 > chapter > book.chapters):
        raise Exception('Bible.py:find_max_verse(): real chapter required')

    path = os.path.join(BIBLE_NUMERICAL_MAP, str(book.value))
    if not os.path.exists(path):
        raise Exception(f'Bible.py:find_max_verse(): Path does not exist. path: {path}')
    
    with open(path, 'r', encoding='utf-8') as file:
        line_num = 1
        for line in file:
            if(line_num == chapter):
                return int(line.split(':')[2])
            line_num += 1
    
    raise Exception('Bible.py:find_max_verse(): unreachable code path reached. BIBLE_NUMERICAL_MAP is broken!')