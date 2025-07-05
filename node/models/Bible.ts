import * as fs from 'fs';
import * as path from 'path';


const BIBLE_NUMERICAL_MAP = path.join(import.meta.dirname, '..', '..', '..', 'bible_numerical_map');

export class Book {
    constructor(
        public readonly name: string,           // e.g: 'Genesis'
        public readonly abbr: string,           // most common abbreviation, e.g: 'Gen'
        public readonly index: number,          // numerical appearance in the bible, 1-66
        public readonly chapters: number,       // total chapters, e.g. 50
    ) {}
    
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

    private static _Books: Book[];

    public static Books(): Book[] {
        if (!BIBLE._Books) {
            BIBLE._Books = Object.values(BIBLE).filter(
                (book): book is Book => book instanceof Book
            );
        }
        return BIBLE._Books;
    }

    /**
     *  Returns a `BIBLE.Book` or `null`, if no match is found:
     *  - `string`: matches `Book.name` (e.g: 'Genesis') or `Book.abbr` (e.g: 'Gen')
     *  - `number`: matches `Book.index` (e.g: 1 for Genesis, 66 for Revelation)
     */
    static getBook(book: string | number): Book | null {
        if (typeof book === 'number') {
            return BIBLE.Books().find(b => b.index === (book - 1)) || null;
        }

        if (typeof book === 'string') {
            const lookup = book.trim().toLowerCase();
            return BIBLE.Books().find(
                b => b.name.toLowerCase() === lookup || b.abbr.toLowerCase() === lookup
            ) || null;
        }
        
        return null;
    }


    static parseChapter(chapter: string | number): number | null {
        if (typeof chapter === 'string')
            chapter = parseInt(chapter, 10);

        if (typeof chapter !== 'number')
            return null;


    }
    
    static findMaxVerse(book: Book, chapter: number): number {
        assert_class('book', book, Book);
        assert_number('chapter', chapter, 1, book.chapters);

        // return;
        
        const filePath = path.join(BIBLE_NUMERICAL_MAP, String(book.index));
        // assertPathExists('path', filePath);
        
        const lines = fs.readFileSync(filePath, 'utf-8').split(/\r?\n/);
        for (let i = 0; i < lines.length; i++) {
            if (i + 1 === chapter) {
                const parts = lines[i].split(':');
                // assuming verse count is at index 2
                const verseCount = parseInt(parts[2], 10);
                if (isNaN(verseCount)) {
                    throw new Error('Invalid verse count in file');
                }
                return verseCount;
            }
        }
        throw new Error(
            'BIBLE.findMaxVerse(): unreachable code path reached. BIBLE_NUMERICAL_MAP is broken!'
        );
    }
}

/**
 *  A BibleReference
 * 
 *  To create, use static contructor: `BibleReference.fromStr("Genesis:5:1")`
 * 
 *  Use: `bibleRef.valid`, to check whether the instance refers to a real bible, that actually exists
 */
export class BibleReference {
    private constructor(
        public book: Book,
        public chapter: number,
        public verse?: number
    ) {}


    /**
     *  Static Constructor
     * @param string - e.g: `"Genesis:5"` or `"Gen:5"`
     */
    static fromStr(string:string): BibleReference | null  {
        const strArray = string.split(':');

        if (strArray.length < 2)
            return null;

        BIBLE.getBook(strArray[0])

        return null;
    }
}