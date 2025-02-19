from dataclasses import dataclass
from enum import Enum

class Books(Enum):
    GENESIS              =  1
    EXODUS               =  2
    LEVITICUS            =  3
    NUMBERS              =  4
    DEUTERONOMY          =  5
    JOSHUA               =  6
    JUDGES               =  7
    RUTH                 =  8
    FIRST_SAMUEL         =  9
    SECOND_SAMUEL        =  10
    FIRST_KINGS          =  11
    SECOND_KINGS         =  12
    FIRST_CHRONICLES     =  13
    SECOND_CHRONICLES    =  14
    EZRA                 =  15
    NEHEMIAH             =  16
    ESTHER               =  17
    JOB                  =  18
    PSALMS               =  19
    PROVERBS             =  20
    ECCLESIASTES         =  21
    SONG_OF_SOLOMON      =  22
    ISAIAH               =  23
    JEREMIAH             =  24
    LAMENTATIONS         =  25
    EZEKIEL              =  26
    DANIEL               =  27
    HOSEA                =  28
    JOEL                 =  29
    AMOS                 =  30
    OBADIAH              =  31
    JONAH                =  32
    MICAH                =  33
    NAHUM                =  34
    HABAKKUK             =  35
    ZEPHANIAH            =  36
    HAGGAI               =  37
    ZECHARIAH            =  38
    MALACHI              =  39
    MATTHEW              =  40
    MARK                 =  41
    LUKE                 =  42
    JOHN                 =  43
    ACTS                 =  44
    ROMANS               =  45
    FIRST_CORINTHIANS    =  46
    SECOND_CORINTHIANS   =  47
    GALATIANS            =  48
    EPHESIANS            =  49
    PHILIPPIANS          =  50
    COLOSSIANS           =  51
    FIRST_THESSALONIANS  =  52
    SECOND_THESSALONIANS =  53
    FIRST_TIMOTHY        =  54
    SECOND_TIMOTHY       =  55
    TITUS                =  56
    PHILEMON             =  57
    HEBREWS              =  58
    JAMES                =  59
    FIRST_PETER          =  60
    SECOND_PETER         =  61
    FIRST_JOHN           =  62
    SECOND_JOHN          =  63
    THIRD_JOHN           =  64
    JUDE                 =  65
    REVELATION           =  66

def toString(book: Books) -> str:
    match book:
        case Books.GENESIS:
            return 'Genesis'
        case Books.EXODUS:
            return 'Exodus'
        case Books.LEVITICUS:
            return 'Leviticus'
        case Books.NUMBERS:
            return 'Numbers'
        case Books.DEUTERONOMY:
            return 'Deuteronomy'
        case Books.JOSHUA:
            return 'Joshua'
        case Books.JUDGES:
            return 'Judges'
        case Books.RUTH:
            return 'Ruth'
        case Books.FIRST_SAMUEL:
            return '1 Samuel'
        case Books.SECOND_SAMUEL:
            return '2 Samuel'
        case Books.FIRST_KINGS:
            return '1 Kings'
        case Books.SECOND_KINGS:
            return '2 Kings'
        case Books.FIRST_CHRONICLES:
            return '1 Chronicles'
        case Books.SECOND_CHRONICLES:
            return '2 Chronicles'
        case Books.EZRA:
            return 'Ezra'
        case Books.NEHEMIAH:
            return 'Nehemiah'
        case Books.ESTHER:
            return 'Esther'
        case Books.JOB:
            return 'Job'
        case Books.PSALMS:
            return 'Psalms'
        case Books.PROVERBS:
            return 'Proverbs'
        case Books.ECCLESIASTES:
            return 'Ecclesiastes'
        case Books.SONG_OF_SOLOMON:
            return 'Song of Solomon'
        case Books.ISAIAH:
            return 'Isaiah'
        case Books.JEREMIAH:
            return 'Jeremiah'
        case Books.LAMENTATIONS:
            return 'Lamentations'
        case Books.EZEKIEL:
            return 'Ezekiel'
        case Books.DANIEL:
            return 'Daniel'
        case Books.HOSEA:
            return 'Hosea'
        case Books.JOEL:
            return 'Joel'
        case Books.AMOS:
            return 'Amos'
        case Books.OBADIAH:
            return 'Obadiah'
        case Books.JONAH:
            return 'Jonah'
        case Books.MICAH:
            return 'Micah'
        case Books.NAHUM:
            return 'Nahum'
        case Books.HABAKKUK:
            return 'Habakkuk'
        case Books.ZEPHANIAH:
            return 'Zephaniah'
        case Books.HAGGAI:
            return 'Haggai'
        case Books.ZECHARIAH:
            return 'Zechariah'
        case Books.MALACHI:
            return 'Malachi'
        case Books.MATTHEW:
            return 'Matthew'
        case Books.MARK:
            return 'Mark'
        case Books.LUKE:
            return 'Luke'
        case Books.JOHN:
            return 'John'
        case Books.ACTS:
            return 'Acts'
        case Books.ROMANS:
            return 'Romans'
        case Books.FIRST_CORINTHIANS:
            return '1 Corinthians'
        case Books.SECOND_CORINTHIANS:
            return '2 Corinthians'
        case Books.GALATIANS:
            return 'Galatians'
        case Books.EPHESIANS:
            return 'Ephesians'
        case Books.PHILIPPIANS:
            return 'Philippians'
        case Books.COLOSSIANS:
            return 'Colossians'
        case Books.FIRST_THESSALONIANS:
            return '1 Thessalonians'
        case Books.SECOND_THESSALONIANS:
            return '2 Thessalonians'
        case Books.FIRST_TIMOTHY:
            return '1 Timothy'
        case Books.SECOND_TIMOTHY:
            return '2 Timothy'
        case Books.TITUS:
            return 'Titus'
        case Books.PHILEMON:
            return 'Philemon'
        case Books.HEBREWS:
            return 'Hebrews'
        case Books.JAMES:
            return 'James'
        case Books.FIRST_PETER:
            return '1 Peter'
        case Books.SECOND_PETER:
            return '2 Peter'
        case Books.FIRST_JOHN:
            return '1 John'
        case Books.SECOND_JOHN:
            return '2 John'
        case Books.THIRD_JOHN:
            return '3 John'
        case Books.JUDE:
            return 'Jude'
        case Books.REVELATION:
            return 'Revelation'
        case _:
            raise RuntimeError(f'Unreachable path reached. Check Bible.py:toString(book: Books)')
        
@dataclass
class BibleBook:
    name: str
    abbr: str
    chapters: int
    index: int

bible_books: dict[Books, BibleBook] = {
    Books.GENESIS:               BibleBook(name='Genesis',            abbr='Gen',      chapters=50,   index=1),
    Books.EXODUS:                BibleBook(name='Exodus',             abbr='Exod',     chapters=40,   index=2),
    Books.LEVITICUS:             BibleBook(name='Leviticus',          abbr='Lev',      chapters=27,   index=3),
    Books.NUMBERS:               BibleBook(name='Numbers',            abbr='Num',      chapters=36,   index=4),
    Books.DEUTERONOMY:           BibleBook(name='Deuteronomy',        abbr='Deut',     chapters=34,   index=5),
    Books.JOSHUA:                BibleBook(name='Joshua',             abbr='Josh',     chapters=24,   index=6),
    Books.JUDGES:                BibleBook(name='Judges',             abbr='Judg',     chapters=21,   index=7),
    Books.RUTH:                  BibleBook(name='Ruth',               abbr='Ruth',     chapters=4,    index=8),
    Books.FIRST_SAMUEL:          BibleBook(name='1 Samuel',           abbr='1Sam',     chapters=31,   index=9),
    Books.SECOND_SAMUEL:         BibleBook(name='2 Samuel',           abbr='2Sam',     chapters=24,   index=10),
    Books.FIRST_KINGS:           BibleBook(name='1 Kings',            abbr='1Kgs',     chapters=22,   index=11),
    Books.SECOND_KINGS:          BibleBook(name='2 Kings',            abbr='2Kgs',     chapters=25,   index=12),
    Books.FIRST_CHRONICLES:      BibleBook(name='1 Chronicles',       abbr='1Chr',     chapters=29,   index=13),
    Books.SECOND_CHRONICLES:     BibleBook(name='2 Chronicles',       abbr='2Chr',     chapters=36,   index=14),
    Books.EZRA:                  BibleBook(name='Ezra',               abbr='Ezra',     chapters=10,   index=15),
    Books.NEHEMIAH:              BibleBook(name='Nehemiah',           abbr='Neh',      chapters=13,   index=16),
    Books.ESTHER:                BibleBook(name='Esther',             abbr='Esth',     chapters=10,   index=17),
    Books.JOB:                   BibleBook(name='Job',                abbr='Job',      chapters=42,   index=18),
    Books.PSALMS:                BibleBook(name='Psalms',             abbr='Ps',       chapters=150,  index=19),
    Books.PROVERBS:              BibleBook(name='Proverbs',           abbr='Prov',     chapters=31,   index=20),
    Books.ECCLESIASTES:          BibleBook(name='Ecclesiastes',       abbr='Eccl',     chapters=12,   index=21),
    Books.SONG_OF_SOLOMON:       BibleBook(name='Song of Solomon',    abbr='Song',     chapters=8,    index=22),
    Books.ISAIAH:                BibleBook(name='Isaiah',             abbr='Isa',      chapters=66,   index=23),
    Books.JEREMIAH:              BibleBook(name='Jeremiah',           abbr='Jer',      chapters=52,   index=24),
    Books.LAMENTATIONS:          BibleBook(name='Lamentations',       abbr='Lam',      chapters=5,    index=25),
    Books.EZEKIEL:               BibleBook(name='Ezekiel',            abbr='Ezek',     chapters=48,   index=26),
    Books.DANIEL:                BibleBook(name='Daniel',             abbr='Dan',      chapters=12,   index=27),
    Books.HOSEA:                 BibleBook(name='Hosea',              abbr='Hos',      chapters=14,   index=28),
    Books.JOEL:                  BibleBook(name='Joel',               abbr='Joel',     chapters=3,    index=29),
    Books.AMOS:                  BibleBook(name='Amos',               abbr='Amos',     chapters=9,    index=30),
    Books.OBADIAH:               BibleBook(name='Obadiah',            abbr='Obad',     chapters=1,    index=31),
    Books.JONAH:                 BibleBook(name='Jonah',              abbr='Jonah',    chapters=4,    index=32),
    Books.MICAH:                 BibleBook(name='Micah',              abbr='Mic',      chapters=7,    index=33),
    Books.NAHUM:                 BibleBook(name='Nahum',              abbr='Nah',      chapters=3,    index=34),
    Books.HABAKKUK:              BibleBook(name='Habakkuk',           abbr='Hab',      chapters=3,    index=35),
    Books.ZEPHANIAH:             BibleBook(name='Zephaniah',          abbr='Zeph',     chapters=3,    index=36),
    Books.HAGGAI:                BibleBook(name='Haggai',             abbr='Hag',      chapters=2,    index=37),
    Books.ZECHARIAH:             BibleBook(name='Zechariah',          abbr='Zech',     chapters=14,   index=38),
    Books.MALACHI:               BibleBook(name='Malachi',            abbr='Mal',      chapters=4,    index=39),
    Books.MATTHEW:               BibleBook(name='Matthew',            abbr='Matt',     chapters=28,   index=40),
    Books.MARK:                  BibleBook(name='Mark',               abbr='Mark',     chapters=16,   index=41),
    Books.LUKE:                  BibleBook(name='Luke',               abbr='Luke',     chapters=24,   index=42),
    Books.JOHN:                  BibleBook(name='John',               abbr='John',     chapters=21,   index=43),
    Books.ACTS:                  BibleBook(name='Acts',               abbr='Acts',     chapters=28,   index=44),
    Books.ROMANS:                BibleBook(name='Romans',             abbr='Rom',      chapters=16,   index=45),
    Books.FIRST_CORINTHIANS:     BibleBook(name='1 Corinthians',      abbr='1Cor',     chapters=16,   index=46),
    Books.SECOND_CORINTHIANS:    BibleBook(name='2 Corinthians',      abbr='2Cor',     chapters=13,   index=47),
    Books.GALATIANS:             BibleBook(name='Galatians',          abbr='Gal',      chapters=6,    index=48),
    Books.EPHESIANS:             BibleBook(name='Ephesians',          abbr='Eph',      chapters=6,    index=49),
    Books.PHILIPPIANS:           BibleBook(name='Philippians',        abbr='Phil',     chapters=4,    index=50),
    Books.COLOSSIANS:            BibleBook(name='Colossians',         abbr='Col',      chapters=4,    index=51),
    Books.FIRST_THESSALONIANS:   BibleBook(name='1 Thessalonians',    abbr='1Thess',   chapters=5,    index=52),
    Books.SECOND_THESSALONIANS:  BibleBook(name='2 Thessalonians',    abbr='2Thess',   chapters=3,    index=53),
    Books.FIRST_TIMOTHY:         BibleBook(name='1 Timothy',          abbr='1Tim',     chapters=6,    index=54),
    Books.SECOND_TIMOTHY:        BibleBook(name='2 Timothy',          abbr='2Tim',     chapters=4,    index=55),
    Books.TITUS:                 BibleBook(name='Titus',              abbr='Titus',    chapters=3,    index=56),
    Books.PHILEMON:              BibleBook(name='Philemon',           abbr='Phlm',     chapters=1,    index=57),
    Books.HEBREWS:               BibleBook(name='Hebrews',            abbr='Heb',      chapters=13,   index=58),
    Books.JAMES:                 BibleBook(name='James',              abbr='Jas',      chapters=5,    index=59),
    Books.FIRST_PETER:           BibleBook(name='1 Peter',            abbr='1Pet',     chapters=5,    index=60),
    Books.SECOND_PETER:          BibleBook(name='2 Peter',            abbr='2Pet',     chapters=3,    index=61),
    Books.FIRST_JOHN:            BibleBook(name='1 John',             abbr='1John',    chapters=5,    index=62),
    Books.SECOND_JOHN:           BibleBook(name='2 John',             abbr='2John',    chapters=1,    index=63),
    Books.THIRD_JOHN:            BibleBook(name='3 John',             abbr='3John',    chapters=1,    index=64),
    Books.JUDE:                  BibleBook(name='Jude',               abbr='Jude',     chapters=1,    index=65),
    Books.REVELATION:            BibleBook(name='Revelation',         abbr='Rev',      chapters=22,   index=66)
}