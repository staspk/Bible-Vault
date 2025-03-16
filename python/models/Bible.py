from dataclasses import dataclass
from enum import Enum

@dataclass
class Book:
    """
     abbreviations for apocrypha
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
    name: str
    abbr: str           # common abbreviation, consistent with BibleGateway abbr's (tested) and 
    chapters: int       # total chapters in book
    index: int          # numerical appearance in the bible, 1-66


class BIBLE(Enum):
    GENESIS               =  'Genesis'
    EXODUS                =  'Exodus'
    LEVITICUS             =  'Leviticus'
    NUMBERS               =  'Numbers'
    DEUTERONOMY           =  'Deuteronomy'
    JOSHUA                =  'Joshua'
    JUDGES                =  'Judges'
    RUTH                  =  'Ruth'
    FIRST_SAMUEL          =  '1 Samuel'
    SECOND_SAMUEL         =  '2 Samuel'
    FIRST_KINGS           =  '1 Kings'
    SECOND_KINGS          =  '2 Kings'
    FIRST_CHRONICLES      =  '1 Chronicles'
    SECOND_CHRONICLES     =  '2 Chronicles'
    EZRA                  =  'Ezra'
    NEHEMIAH              =  'Nehemiah'
    ESTHER                =  'Esther'
    JOB                   =  'Job'
    PSALMS                =  'Psalms'
    PROVERBS              =  'Proverbs'
    ECCLESIASTES          =  'Ecclesiastes'
    SONG_OF_SOLOMON       =  'Song of Solomon'
    ISAIAH                =  'Isaiah'
    JEREMIAH              =  'Jeremiah'
    LAMENTATIONS          =  'Lamentations'
    EZEKIEL               =  'Ezekiel'
    DANIEL                =  'Daniel'
    HOSEA                 =  'Hosea'
    JOEL                  =  'Joel'
    AMOS                  =  'Amos'
    OBADIAH               =  'Obadiah'
    JONAH                 =  'Jonah'
    MICAH                 =  'Micah'
    NAHUM                 =  'Nahum'
    HABAKKUK              =  'Habakkuk'
    ZEPHANIAH             =  'Zephaniah'
    HAGGAI                =  'Haggai'
    ZECHARIAH             =  'Zechariah'
    MALACHI               =  'Malachi'
    MATTHEW               =  'Matthew'
    MARK                  =  'Mark'
    LUKE                  =  'Luke'
    JOHN                  =  'John'
    ACTS                  =  'Acts'
    ROMANS                =  'Romans'
    FIRST_CORINTHIANS     =  '1 Corinthians'
    SECOND_CORINTHIANS    =  '2 Corinthians'
    GALATIANS             =  'Galatians'
    EPHESIANS             =  'Ephesians'
    PHILIPPIANS           =  'Philippians'
    COLOSSIANS            =  'Colossians'
    FIRST_THESSALONIANS   =  '1 Thessalonians'
    SECOND_THESSALONIANS  =  '2 Thessalonians'
    FIRST_TIMOTHY         =  '1 Timothy'
    SECOND_TIMOTHY        =  '2 Timothy'
    TITUS                 =  'Titus'
    PHILEMON              =  'Philemon'
    HEBREWS               =  'Hebrews'
    JAMES                 =  'James'
    FIRST_PETER           =  '1 Peter'
    SECOND_PETER          =  '2 Peter'
    FIRST_JOHN            =  '1 John'
    SECOND_JOHN           =  '2 John'
    THIRD_JOHN            =  '3 John'
    JUDE                  =  'Jude'
    REVELATION            =  'Revelation'


Bible: dict[BIBLE, Book] = {
    BIBLE.GENESIS:               Book(name=BIBLE.GENESIS.name,               abbr='Gen',      chapters=50,    index=1),
    BIBLE.EXODUS:                Book(name=BIBLE.EXODUS.name,                abbr='Exod',     chapters=40,    index=2),
    BIBLE.LEVITICUS:             Book(name=BIBLE.LEVITICUS.name,             abbr='Lev',      chapters=27,    index=3),
    BIBLE.NUMBERS:               Book(name=BIBLE.NUMBERS.name,               abbr='Num',      chapters=36,    index=4),
    BIBLE.DEUTERONOMY:           Book(name=BIBLE.DEUTERONOMY.name,           abbr='Deut',     chapters=34,    index=5),
    BIBLE.JOSHUA:                Book(name=BIBLE.JOSHUA.name,                abbr='Josh',     chapters=24,    index=6),
    BIBLE.JUDGES:                Book(name=BIBLE.JUDGES.name,                abbr='Judg',     chapters=21,    index=7),
    BIBLE.RUTH:                  Book(name=BIBLE.RUTH.name,                  abbr='Ruth',     chapters=4,     index=8),
    BIBLE.FIRST_SAMUEL:          Book(name=BIBLE.FIRST_SAMUEL.name,          abbr='1Sam',     chapters=31,    index=9),
    BIBLE.SECOND_SAMUEL:         Book(name=BIBLE.SECOND_SAMUEL.name,         abbr='2Sam',     chapters=24,    index=10),
    BIBLE.FIRST_KINGS:           Book(name=BIBLE.FIRST_KINGS.name,           abbr='1Kgs',     chapters=22,    index=11),
    BIBLE.SECOND_KINGS:          Book(name=BIBLE.SECOND_KINGS.name,          abbr='2Kgs',     chapters=25,    index=12),
    BIBLE.FIRST_CHRONICLES:      Book(name=BIBLE.FIRST_CHRONICLES.name,      abbr='1Chr',     chapters=29,    index=13),
    BIBLE.SECOND_CHRONICLES:     Book(name=BIBLE.SECOND_CHRONICLES.name,     abbr='2Chr',     chapters=36,    index=14),
    BIBLE.EZRA:                  Book(name=BIBLE.EZRA.name,                  abbr='Ezra',     chapters=10,    index=15),
    BIBLE.NEHEMIAH:              Book(name=BIBLE.NEHEMIAH.name,              abbr='Neh',      chapters=13,    index=16),
    BIBLE.ESTHER:                Book(name=BIBLE.ESTHER.name,                abbr='Esth',     chapters=10,    index=17),
    BIBLE.JOB:                   Book(name=BIBLE.JOB.name,                   abbr='Job',      chapters=42,    index=18),
    BIBLE.PSALMS:                Book(name=BIBLE.PSALMS.name,                abbr='Ps',       chapters=150,   index=19),
    BIBLE.PROVERBS:              Book(name=BIBLE.PROVERBS.name,              abbr='Prov',     chapters=31,    index=20),
    BIBLE.ECCLESIASTES:          Book(name=BIBLE.ECCLESIASTES.name,          abbr='Eccl',     chapters=12,    index=21),
    BIBLE.SONG_OF_SOLOMON:       Book(name=BIBLE.SONG_OF_SOLOMON.name,       abbr='Song',     chapters=8,     index=22),
    BIBLE.ISAIAH:                Book(name=BIBLE.ISAIAH.name,                abbr='Isa',      chapters=66,    index=23),
    BIBLE.JEREMIAH:              Book(name=BIBLE.JEREMIAH.name,              abbr='Jer',      chapters=52,    index=24),
    BIBLE.LAMENTATIONS:          Book(name=BIBLE.LAMENTATIONS.name,          abbr='Lam',      chapters=5,     index=25),
    BIBLE.EZEKIEL:               Book(name=BIBLE.EZEKIEL.name,               abbr='Ezek',     chapters=48,    index=26),
    BIBLE.DANIEL:                Book(name=BIBLE.DANIEL.name,                abbr='Dan',      chapters=12,    index=27),
    BIBLE.HOSEA:                 Book(name=BIBLE.HOSEA.name,                 abbr='Hos',      chapters=14,    index=28),
    BIBLE.JOEL:                  Book(name=BIBLE.JOEL.name,                  abbr='Joel',     chapters=3,     index=29),
    BIBLE.AMOS:                  Book(name=BIBLE.AMOS.name,                  abbr='Amos',     chapters=9,     index=30),
    BIBLE.OBADIAH:               Book(name=BIBLE.OBADIAH.name,               abbr='Obad',     chapters=1,     index=31),
    BIBLE.JONAH:                 Book(name=BIBLE.JONAH.name,                 abbr='Jonah',    chapters=4,     index=32),
    BIBLE.MICAH:                 Book(name=BIBLE.MICAH.name,                 abbr='Mic',      chapters=7,     index=33),
    BIBLE.NAHUM:                 Book(name=BIBLE.NAHUM.name,                 abbr='Nah',      chapters=3,     index=34),
    BIBLE.HABAKKUK:              Book(name=BIBLE.HABAKKUK.name,              abbr='Hab',      chapters=3,     index=35),
    BIBLE.ZEPHANIAH:             Book(name=BIBLE.ZEPHANIAH.name,             abbr='Zeph',     chapters=3,     index=36),
    BIBLE.HAGGAI:                Book(name=BIBLE.HAGGAI.name,                abbr='Hag',      chapters=2,     index=37),
    BIBLE.ZECHARIAH:             Book(name=BIBLE.ZECHARIAH.name,             abbr='Zech',     chapters=14,    index=38),
    BIBLE.MALACHI:               Book(name=BIBLE.MALACHI.name,               abbr='Mal',      chapters=4,     index=39),
    BIBLE.MATTHEW:               Book(name=BIBLE.MATTHEW.name,               abbr='Matt',     chapters=28,    index=40),
    BIBLE.MARK:                  Book(name=BIBLE.MARK.name,                  abbr='Mark',     chapters=16,    index=41),
    BIBLE.LUKE:                  Book(name=BIBLE.LUKE.name,                  abbr='Luke',     chapters=24,    index=42),
    BIBLE.JOHN:                  Book(name=BIBLE.JOHN.name,                  abbr='John',     chapters=21,    index=43),
    BIBLE.ACTS:                  Book(name=BIBLE.ACTS.name,                  abbr='Acts',     chapters=28,    index=44),
    BIBLE.ROMANS:                Book(name=BIBLE.ROMANS.name,                abbr='Rom',      chapters=16,    index=45),
    BIBLE.FIRST_CORINTHIANS:     Book(name=BIBLE.FIRST_CORINTHIANS.name,     abbr='1Cor',     chapters=16,    index=46),
    BIBLE.SECOND_CORINTHIANS:    Book(name=BIBLE.SECOND_CORINTHIANS.name,    abbr='2Cor',     chapters=13,    index=47),
    BIBLE.GALATIANS:             Book(name=BIBLE.GALATIANS.name,             abbr='Gal',      chapters=6,     index=48),
    BIBLE.EPHESIANS:             Book(name=BIBLE.EPHESIANS.name,             abbr='Eph',      chapters=6,     index=49),
    BIBLE.PHILIPPIANS:           Book(name=BIBLE.PHILIPPIANS.name,           abbr='Phil',     chapters=4,     index=50),
    BIBLE.COLOSSIANS:            Book(name=BIBLE.COLOSSIANS.name,            abbr='Col',      chapters=4,     index=51),
    BIBLE.FIRST_THESSALONIANS:   Book(name=BIBLE.FIRST_THESSALONIANS.name,   abbr='1Thess',   chapters=5,     index=52),
    BIBLE.SECOND_THESSALONIANS:  Book(name=BIBLE.SECOND_THESSALONIANS.name,  abbr='2Thess',   chapters=3,     index=53),
    BIBLE.FIRST_TIMOTHY:         Book(name=BIBLE.FIRST_TIMOTHY.name,         abbr='1Tim',     chapters=6,     index=54),
    BIBLE.SECOND_TIMOTHY:        Book(name=BIBLE.SECOND_TIMOTHY.name,        abbr='2Tim',     chapters=4,     index=55),
    BIBLE.TITUS:                 Book(name=BIBLE.TITUS.name,                 abbr='Titus',    chapters=3,     index=56),
    BIBLE.PHILEMON:              Book(name=BIBLE.PHILEMON.name,              abbr='Phlm',     chapters=1,     index=57),
    BIBLE.HEBREWS:               Book(name=BIBLE.HEBREWS.name,               abbr='Heb',      chapters=13,    index=58),
    BIBLE.JAMES:                 Book(name=BIBLE.JAMES.name,                 abbr='Jas',      chapters=5,     index=59),
    BIBLE.FIRST_PETER:           Book(name=BIBLE.FIRST_PETER.name,           abbr='1Pet',     chapters=5,     index=60),
    BIBLE.SECOND_PETER:          Book(name=BIBLE.SECOND_PETER.name,          abbr='2Pet',     chapters=3,     index=61),
    BIBLE.FIRST_JOHN:            Book(name=BIBLE.FIRST_JOHN.name,            abbr='1John',    chapters=5,     index=62),
    BIBLE.SECOND_JOHN:           Book(name=BIBLE.SECOND_JOHN.name,           abbr='2John',    chapters=1,     index=63),
    BIBLE.THIRD_JOHN:            Book(name=BIBLE.THIRD_JOHN.name,            abbr='3John',    chapters=1,     index=64),
    BIBLE.JUDE:                  Book(name=BIBLE.JUDE.name,                  abbr='Jude',     chapters=1,     index=65),
    BIBLE.REVELATION:            Book(name=BIBLE.REVELATION.name,            abbr='Rev',      chapters=22,    index=66)
}
