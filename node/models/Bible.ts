import * as fs from 'fs';
import * as path from 'path';

import { assert_number, assert_class } from './../kozubenko/typing.ts';


const BIBLE_NUMERICAL_MAP = path.join(__dirname, '..', '..', '..', 'bible_numerical_map');

/**
    * name: string — e.g. 'Genesis'
    * abbr: string — consistent with BibleGateway abbreviations
    * chapters: number — total chapters, e.g. 50
    * index: number — numerical appearance in the bible, 1-66
*/
export class Book {
    constructor(
        public name: string,
        public abbr: string,
        public chapters: number,
        public index: number
    ) {}
    
    toString() {
        return this.name;
    }
}

export class BIBLE {
    static GENESIS              = new Book('Genesis',             'Gen',      50, 1);
    static EXODUS               = new Book('Exodus',              'Exod',     40, 2);
    static LEVITICUS            = new Book('Leviticus',           'Lev',      27, 3);
    static NUMBERS              = new Book('Numbers',             'Num',      36, 4);
    static DEUTERONOMY          = new Book('Deuteronomy',         'Deut',     34, 5);
    static JOSHUA               = new Book('Joshua',              'Josh',     24, 6);
    static JUDGES               = new Book('Judges',              'Judg',     21, 7);
    static RUTH                 = new Book('Ruth',                'Ruth',     4,  8);
    static FIRST_SAMUEL         = new Book('1 Samuel',            '1Sam',     31, 9);
    static SECOND_SAMUEL        = new Book('2 Samuel',            '2Sam',     24, 10);
    static FIRST_KINGS          = new Book('1 Kings',             '1Kgs',     22, 11);
    static SECOND_KINGS         = new Book('2 Kings',             '2Kgs',     25, 12);
    static FIRST_CHRONICLES     = new Book('1 Chronicles',        '1Chr',     29, 13);
    static SECOND_CHRONICLES    = new Book('2 Chronicles',        '2Chr',     36, 14);
    static EZRA                 = new Book('Ezra',                'Ezra',     10, 15);
    static NEHEMIAH             = new Book('Nehemiah',            'Neh',      13, 16);
    static ESTHER               = new Book('Esther',              'Esth',     10, 17);
    static JOB                  = new Book('Job',                 'Job',      42, 18);
    static PSALMS               = new Book('Psalms',              'Ps',       150,19);
    static PROVERBS             = new Book('Proverbs',            'Prov',     31, 20);
    static ECCLESIASTES         = new Book('Ecclesiastes',        'Eccl',     12, 21);
    static SONG_OF_SOLOMON      = new Book('Song of Solomon',     'Song',     8,  22);
    static ISAIAH               = new Book('Isaiah',              'Isa',      66, 23);
    static JEREMIAH             = new Book('Jeremiah',            'Jer',      52, 24);
    static LAMENTATIONS         = new Book('Lamentations',        'Lam',      5,  25);
    static EZEKIEL              = new Book('Ezekiel',             'Ezek',     48, 26);
    static DANIEL               = new Book('Daniel',              'Dan',      12, 27);
    static HOSEA                = new Book('Hosea',               'Hos',      14, 28);
    static JOEL                 = new Book('Joel',                'Joel',     3,  29);
    static AMOS                 = new Book('Amos',                'Amos',     9,  30);
    static OBADIAH              = new Book('Obadiah',             'Obad',     1,  31);
    static JONAH                = new Book('Jonah',               'Jonah',    4,  32);
    static MICAH                = new Book('Micah',               'Mic',      7,  33);
    static NAHUM                = new Book('Nahum',               'Nah',      3,  34);
    static HABAKKUK             = new Book('Habakkuk',            'Hab',      3,  35);
    static ZEPHANIAH            = new Book('Zephaniah',           'Zeph',     3,  36);
    static HAGGAI               = new Book('Haggai',              'Hag',      2,  37);
    static ZECHARIAH            = new Book('Zechariah',           'Zech',     14, 38);
    static MALACHI              = new Book('Malachi',             'Mal',      4,  39);
    static MATTHEW              = new Book('Matthew',             'Matt',     28, 40);
    static MARK                 = new Book('Mark',                'Mark',     16, 41);
    static LUKE                 = new Book('Luke',                'Luke',     24, 42);
    static JOHN                 = new Book('John',                'John',     21, 43);
    static ACTS                 = new Book('Acts',                'Acts',     28, 44);
    static ROMANS               = new Book('Romans',              'Rom',      16, 45);
    static FIRST_CORINTHIANS    = new Book('1 Corinthians',       '1Cor',     16, 46);
    static SECOND_CORINTHIANS   = new Book('2 Corinthians',       '2Cor',     13, 47);
    static GALATIANS            = new Book('Galatians',           'Gal',      6,  48);
    static EPHESIANS            = new Book('Ephesians',           'Eph',      6,  49);
    static PHILIPPIANS          = new Book('Philippians',         'Phil',     4,  50);
    static COLOSSIANS           = new Book('Colossians',          'Col',      4,  51);
    static FIRST_THESSALONIANS  = new Book('1 Thessalonians',     '1Thess',   5,  52);
    static SECOND_THESSALONIANS = new Book('2 Thessalonians',     '2Thess',   3,  53);
    static FIRST_TIMOTHY        = new Book('1 Timothy',           '1Tim',     6,  54);
    static SECOND_TIMOTHY       = new Book('2 Timothy',           '2Tim',     4,  55);
    static TITUS                = new Book('Titus',               'Titus',    3,  56);
    static PHILEMON             = new Book('Philemon',            'Phlm',     1,  57);
    static HEBREWS              = new Book('Hebrews',             'Heb',      13, 58);
    static JAMES                = new Book('James',               'Jas',      5,  59);
    static FIRST_PETER          = new Book('1 Peter',             '1Pet',     5,  60);
    static SECOND_PETER         = new Book('2 Peter',             '2Pet',     3,  61);
    static FIRST_JOHN           = new Book('1 John',              '1John',    5,  62);
    static SECOND_JOHN          = new Book('2 John',              '2John',    1,  63);
    static THIRD_JOHN           = new Book('3 John',              '3John',    1,  64);
    static JUDE                 = new Book('Jude',                'Jude',     1,  65);
    static REVELATION           = new Book('Revelation',          'Rev',      22, 66);
    
    static Books(): Book[] {
        return Object.values(BIBLE).filter(
            (book): book is Book => book instanceof Book
        );
    }
    
    static findMaxVerse(book: Book, chapter: number): number {
        assert_class('book', book, Book);
        assert_number('chapter', chapter, 1, book.chapters);

        return;
        
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