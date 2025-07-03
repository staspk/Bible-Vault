const _BIBLE_SEARCH_TERMS = [
    'Genesis', 'Gen',
    'Exodus',  'Exod',
    'Leviticus', 'Lev',
    'Numbers', 'Num',
    'Deuteronomy', 'Deut',
    'Joshua', 'Josh',
    'Judges', 'Judg',
    'Ruth',
    '1 Samuel', '1 Sam', '1Samuel', '1Sam',
    '2 Samuel', '2 Sam', '2Samuel', '2Sam',
    '1 Kings', '1 Kgs', '1Kings', '1Kgs',
    '2 Kings', '2 Kgs', '2Kings', '2Kgs',
    '1 Chronicles', '1 Chr', '1Chronicles', '1Chr',
    '2 Chronicles', '2 Chr', '2Chronicles', '2Chr',
    'Ezra',
    'Nehemiah', 'Neh',
    'Esther',  'Esth',
    'Job',
    'Psalms', 'Psalm', 'Ps',
    'Proverbs',  'Prov',
    'Ecclesiastes', 'Eccl',
    'Song of Solomon', 'Song', 'Canticle of Canticles', 'Canticles', 'Cant',
    'Isaiah', 'Isa',
    'Jeremiah', 'Jer',
    'Lamentations', 'Lam',
    'Ezekiel', 'Ezek',
    'Daniel',  'Dan',
    'Hosea',   'Hos',
    'Joel',
    'Amos',
    'Obadiah', 'Obad',
    'Jonah',
    'Micah',    'Mic',
    'Nahum',    'Nah',
    'Habakkuk', 'Hab',
    'Zephaniah', 'Zeph',
    'Haggai',   'Hag',
    'Zechariah', 'Zech',
    'Malachi', 'Mal',
    'Matthew', 'Matt',
    'Mark',
    'Luke',
    'John',
    'Acts',
    'Romans', 'Rom',
    '1 Corinthians', '1 Cor', '1Corinthians', '1Cor',
    '2 Corinthians', '2 Cor', '2Corinthians', '2Cor',
    'Galatians',  'Gal',
    'Ephesians',  'Eph',
    'Philippians', 'Phil',
    'Colossians', 'Col',
    '1 Thessalonians', '1 Thess', '1Thessalonians', '1Thess',
    '2 Thessalonians', '2 Thess', '2Thessalonians', '2Thess',
    '1 Timothy', '1 Tim', '1Timothy', '1Tim',
    '2 Timothy', '2 Tim', '2Timothy', '2Tim',
    'Titus',
    'Philemon', 'Phlm',
    'Hebrews', 'Heb',
    'James',  'Jas',
    '1 Peter', '1 Pet',  '1Peter', '1Pet',
    '2 Peter', '2 Pet',  '2Peter', '2Pet',
    '1 John',  '1 John', '1John',  '1John',
    '2 John',  '2 John', '2John',  '2John',
    '3 John',  '3 John', '3John',  '3John',
    'Jude',
    'Revelation of John', 'Revelations', 'Revelation', 'Rev', 'Apocalypse', 'Apoc',

    // Apocrypha
    'Tobit', 'Tobias', 'Tob',
    'Judith', 'Jdt',
    'Wisdom of Solomon', 'Wisdom', 'Wisd',
    'Sirach', 'Sir', 'Ecclesiasticus',
    'Baruch',
    'Letter of Jeremiah', 'Epistle of Jeremiah',
    'Prayer of Azariah', 'Song of the Three Children', 'Azariah',
    '1 Maccabees', '1 Mac', '1Maccabees', '1Macc',
    '2 Maccabees', '2 Mac', '2Maccabees', '2Macc',
    '3 Maccabees', '3 Mac', '3Maccabees', '3Macc',
    '4 Maccabees', '4 Mac', '4Maccabees', '4Macc',
    'Prayer of Manasseh', 'Manasseh'
];
_BIBLE_SEARCH_TERMS.sort((a, b) => b.length - a.length);    // Sorted longest to shortest. Ensures search algorithm works correctly, e.g: not splitting 'Revelation of John' when search term: 'John'.
export const BIBLE_SEARCH_TERMS = _BIBLE_SEARCH_TERMS;

export class Book {
    constructor(name, abbr, index, chapters) {
        this.name = name;           // e.g: 'Genesis'
        this.abbr = abbr;           // most common abbreviation, e.g: 'Gen'
        this.index = index;         // numerical appearance in the bible, 1-66
        this.chapters = chapters;   // total chapters, e.g. 50
    }

    toString() {
        return this.name;
    }
}

export class BIBLE {
    static GENESIS              = new Book('Genesis',             'Gen',       1,  50);
    static EXODUS               = new Book('Exodus',              'Exod',      2,  40);
    static LEVITICUS            = new Book('Leviticus',           'Lev',       3,  27);
    static NUMBERS              = new Book('Numbers',             'Num',       4,  36);
    static DEUTERONOMY          = new Book('Deuteronomy',         'Deut',      5,  34);
    static JOSHUA               = new Book('Joshua',              'Josh',      6,  24);
    static JUDGES               = new Book('Judges',              'Judg',      7,  21);
    static RUTH                 = new Book('Ruth',                'Ruth',      8,   4);
    static FIRST_SAMUEL         = new Book('1 Samuel',            '1Sam',      9,  31);
    static SECOND_SAMUEL        = new Book('2 Samuel',            '2Sam',     10,  24);
    static FIRST_KINGS          = new Book('1 Kings',             '1Kgs',     11,  22);
    static SECOND_KINGS         = new Book('2 Kings',             '2Kgs',     12,  25);
    static FIRST_CHRONICLES     = new Book('1 Chronicles',        '1Chr',     13,  29);
    static SECOND_CHRONICLES    = new Book('2 Chronicles',        '2Chr',     14,  36);
    static EZRA                 = new Book('Ezra',                'Ezra',     15,  10);
    static NEHEMIAH             = new Book('Nehemiah',            'Neh',      16,  13);
    static ESTHER               = new Book('Esther',              'Esth',     17,  10);
    static JOB                  = new Book('Job',                 'Job',      18,  42);
    static PSALMS               = new Book('Psalms',              'Ps',       19, 150);
    static PROVERBS             = new Book('Proverbs',            'Prov',     20,  31);
    static ECCLESIASTES         = new Book('Ecclesiastes',        'Eccl',     21,  12);
    static SONG_OF_SOLOMON      = new Book('Song of Solomon',     'Song',     22,   8);
    static ISAIAH               = new Book('Isaiah',              'Isa',      23,  66);
    static JEREMIAH             = new Book('Jeremiah',            'Jer',      24,  52);
    static LAMENTATIONS         = new Book('Lamentations',        'Lam',      25,   5);
    static EZEKIEL              = new Book('Ezekiel',             'Ezek',     26,  48);
    static DANIEL               = new Book('Daniel',              'Dan',      27,  12);
    static HOSEA                = new Book('Hosea',               'Hos',      28,  14);
    static JOEL                 = new Book('Joel',                'Joel',     29,   3);
    static AMOS                 = new Book('Amos',                'Amos',     30,   9);
    static OBADIAH              = new Book('Obadiah',             'Obad',     31,   1);
    static JONAH                = new Book('Jonah',               'Jonah',    32,   4);
    static MICAH                = new Book('Micah',               'Mic',      33,   7);
    static NAHUM                = new Book('Nahum',               'Nah',      34,   3);
    static HABAKKUK             = new Book('Habakkuk',            'Hab',      35,   3);
    static ZEPHANIAH            = new Book('Zephaniah',           'Zeph',     36,   3);
    static HAGGAI               = new Book('Haggai',              'Hag',      37,   2);
    static ZECHARIAH            = new Book('Zechariah',           'Zech',     38,  14);
    static MALACHI              = new Book('Malachi',             'Mal',      39,   4);
    static MATTHEW              = new Book('Matthew',             'Matt',     40,  28);
    static MARK                 = new Book('Mark',                'Mark',     41,  16);
    static LUKE                 = new Book('Luke',                'Luke',     42,  24);
    static JOHN                 = new Book('John',                'John',     43,  21);
    static ACTS                 = new Book('Acts',                'Acts',     44,  28);
    static ROMANS               = new Book('Romans',              'Rom',      45,  16);
    static FIRST_CORINTHIANS    = new Book('1 Corinthians',       '1Cor',     46,  16);
    static SECOND_CORINTHIANS   = new Book('2 Corinthians',       '2Cor',     47,  13);
    static GALATIANS            = new Book('Galatians',           'Gal',      48,   6);
    static EPHESIANS            = new Book('Ephesians',           'Eph',      49,   6);
    static PHILIPPIANS          = new Book('Philippians',         'Phil',     50,   4);
    static COLOSSIANS           = new Book('Colossians',          'Col',      51,   4);
    static FIRST_THESSALONIANS  = new Book('1 Thessalonians',     '1Thess',   52,   5);
    static SECOND_THESSALONIANS = new Book('2 Thessalonians',     '2Thess',   53,   3);
    static FIRST_TIMOTHY        = new Book('1 Timothy',           '1Tim',     54,   6);
    static SECOND_TIMOTHY       = new Book('2 Timothy',           '2Tim',     55,   4);
    static TITUS                = new Book('Titus',               'Titus',    56,   3);
    static PHILEMON             = new Book('Philemon',            'Phlm',     57,   1);
    static HEBREWS              = new Book('Hebrews',             'Heb',      58,  13);
    static JAMES                = new Book('James',               'Jas',      59,   5);
    static FIRST_PETER          = new Book('1 Peter',             '1Pet',     60,   5);
    static SECOND_PETER         = new Book('2 Peter',             '2Pet',     61,   3);
    static FIRST_JOHN           = new Book('1 John',              '1John',    62,   5);
    static SECOND_JOHN          = new Book('2 John',              '2John',    63,   1);
    static THIRD_JOHN           = new Book('3 John',              '3John',    64,   1);
    static JUDE                 = new Book('Jude',                'Jude',     65,   1);
    static REVELATION           = new Book('Revelation',          'Rev',      66,  22);
}