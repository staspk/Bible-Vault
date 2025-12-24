import { BIBLE, Book } from "../../../_shared/Bible.js";
import { longest_string_length, removeWhitespace } from "../../../kozubenko/string.extensions.js";


const BOOKS_MAP: Map<string, string[]> = new Map([
    ['1', ['1SAMUEL', '1KINGS', '1CHRONICLES', '1CORINTHIANS', '1THESSALONIANS', '1TIMOTHY', '1PETER', '1JOHN']],
    ['2', ['2SAMUEL', '2KINGS', '2CHRONICLES', '2CORINTHIANS', '2THESSALONIANS', '2TIMOTHY', '2PETER', '2JOHN']],
    ['3', ['3JOHN']],
    ['A', ['AMOS', 'ACTS']],
    ['C', ['COLOSSIANS']],
    ['D', ['DEUTERONOMY', 'DANIEL']],
    ['E', ['EXODUS', 'EZRA', 'ESTHER', 'ECCLESIASTES', 'EZEKIEL', 'EPHESIANS']],
    ['G', ['GENESIS', 'GALATIANS']],
    ['H', ['HOSEA', 'HABAKKUK', 'HAGGAI', 'HEBREWS']],
    ['I', ['ISAIAH']],
    ['J', ['JOSHUA', 'JUDGES', 'JOB', 'JEREMIAH', 'JOEL', 'JONAH', 'JOHN', 'JAMES', 'JUDE']],
    ['L', ['LEVITICUS', 'LAMENTATIONS', 'LUKE']],
    ['M', ['MICAH', 'MALACHI', 'MATTHEW', 'MARK']],
    ['N', ['NUMBERS', 'NEHEMIAH', 'NAHUM']],
    ['O', ['OBADIAH']],
    ['P', ['PSALMS', 'PROVERBS', 'PHILIPPIANS', 'PHILEMON']],
    ['R', ['RUTH', 'ROMANS', 'REVELATION']],
    ['S', ['SONGOFSOLOMON']],
    ['T', ['TITUS']],
    ['Z', ['ZEPHANIAH', 'ZECHARIAH']]
]);

export function BookSearch(search:string): Book|null {
    search = removeWhitespace(search).toUpperCase();

    if(!BOOKS_MAP.has(search[0]))
        return null;

    let possible_valid_searches = BOOKS_MAP.get(search[0]) as string[];

    const MAX_LENGTH = longest_string_length(possible_valid_searches);
    if(search.length > MAX_LENGTH) return null;

    let possible_searches:Set<string> = new Set(possible_valid_searches);
    let ptr = 1;
    while(possible_searches.size > 1) {
        for (const possible of possible_searches) {
            if(search[ptr] !== possible[ptr])
                possible_searches.delete(possible);
        }
        ptr++;
    }

    const result = possible_searches.values().next().value;
    for (const book of BIBLE.Books()) {
        if(result === removeWhitespace(book.name).toUpperCase())
            return book;
    }
    
    return null;
}


/** CURRENTLY DEPRECATED / NOT IN USE */
const BIBLE_BOOK_SEARCH_TERMS = [
    ['Genesis', 'Gen', 'Бытие'],
    ['Exodus', 'Exod', 'Исход'],
    ['Leviticus', 'Lev', 'Левит'],
    ['Numbers', 'Num', 'Числа'],
    ['Deuteronomy', 'Deut', 'Второзаконие'],
    ['Joshua', 'Josh', 'Иисус Навин'],
    ['Judges', 'Judg', 'Книга Судей', 'Судей', 'Судья'],
    ['Ruth', 'Руфь'],
    ['1 Samuel', '1 Sam', '1Samuel', '1Sam', '1-я Царств'],
    ['2 Samuel', '2 Sam', '2Samuel', '2Sam', '2-я Царств'],
    ['1 Kings', '1 Kgs', '1Kings', '1Kgs', '3-я Царств'],
    ['2 Kings', '2 Kgs', '2Kings', '2Kgs', '4-я Царств'],
    ['1 Chronicles', '1 Chr', '1Chronicles', '1Chr', '1-я Паралипоменон'],
    ['2 Chronicles', '2 Chr', '2Chronicles', '2Chr', '2-я Паралипоменон'],
    ['Ezra', 'Ездра'],
    ['Nehemiah', 'Neh', 'Неемия'],
    ['Esther', 'Esth', 'Есфирь'],
    ['Job', 'Иов'],
    ['Psalms', 'Psalm', 'Ps', 'Псалтирь', 'Псалм'],
    ['Proverbs', 'Prov', 'Притчи', 'Притча'],
    ['Ecclesiastes', 'Eccl', 'Екклесиаст', 'Еккл'],
    ['Song of Solomon', 'Song', 'Canticle of Canticles', 'Canticles', 'Cant', 'Песни Песней', 'Песня Песней'],
    ['Isaiah', 'Isa', 'Исаия'],
    ['Jeremiah', 'Jer', 'Иеремия', 'Иеремии'],
    ['Lamentations', 'Lam', 'Плач Иеремии', 'Плач Иеремия', 'Плач'],
    ['Ezekiel', 'Ezek', 'Иезекииль', 'Иезекиил'],
    ['Daniel', 'Dan', 'Даниил'],
    ['Hosea', 'Hos', 'Осия'],
    ['Joel', 'Иоиль'],
    ['Amos', 'Амос'],
    ['Obadiah', 'Obad', 'Авдий'],
    ['Jonah', 'Иона'],
    ['Micah', 'Mic', 'Михей'],
    ['Nahum', 'Nah', 'Наум'],
    ['Habakkuk', 'Hab', 'Аввакум'],
    ['Zephaniah', 'Zeph', 'Софония'],
    ['Haggai', 'Hag', 'Аггей'],
    ['Zechariah', 'Zech', 'Захария'],
    ['Malachi', 'Mal', 'Малахия'],
    ['Matthew', 'Matt', 'От Матфея', 'Матфея'],
    ['Mark', 'От Марка', 'Марка'],
    ['Luke', 'От Луки', 'Луки'],
    ['John', 'От Иоанна', 'Иоанна'],
    ['Acts', 'Деяния'],
    ['Romans', 'Rom', 'Римлянам'],
    ['1 Corinthians', '1 Cor', '1Corinthians', '1Cor', '1 Коринфянам'],
    ['2 Corinthians', '2 Cor', '2Corinthians', '2Cor', '2 Коринфянам'],
    ['Galatians', 'Gal', 'К Галатам'],
    ['Ephesians', 'Eph', 'К Ефесянам'],
    ['Philippians', 'Phil', 'К Филиппийцам'],
    ['Colossians', 'Col', 'К Колоссянам'],
    ['1 Thessalonians', '1 Thess', '1Thessalonians', '1Thess', '1 Фессалоникийцам'],
    ['2 Thessalonians', '2 Thess', '2Thessalonians', '2Thess', '2 Фессалоникийцам'],
    ['1 Timothy', '1 Tim', '1Timothy', '1Tim', '1 Тимофею', '1 Тимофея'],
    ['2 Timothy', '2 Tim', '2Timothy', '2Tim', '2 Тимофею', '2 Тимофея'],
    ['Titus', 'К Титу'],
    ['Philemon', 'Phlm', 'К Филимону'],
    ['Hebrews', 'Heb', 'К Евреям'],
    ['James', 'Jas', 'Иакова'],
    ['1 Peter', '1 Pet', '1Peter', '1Pet', '1 Петра'],
    ['2 Peter', '2 Pet', '2Peter', '2Pet', '2 Петра'],
    ['1 John', '1 John', '1John', '1John', '1 Иоанна'],
    ['2 John', '2 John', '2John', '2John', '2 Иоанна'],
    ['3 John', '3 John', '3John', '3John', '3 Иоанна'],
    ['Jude', 'Иуды'],
    ['Revelation of John', 'Revelations', 'Revelation', 'Rev', 'Apocalypse', 'Apoc', 'Откровение Иоанна', 'Откровение'],
        
    // Apocrypha
    ['Tobit', 'Tobias', 'Tob'],
    ['Judith', 'Jdt'],
    ['Wisdom of Solomon', 'Wisdom', 'Wisd'],
    ['Sirach', 'Sir', 'Ecclesiasticus'],
    ['Baruch'],
    ['Letter of Jeremiah', 'Epistle of Jeremiah'],
    ['Prayer of Azariah', 'Song of the Three Children', 'Azariah'],
    ['1 Maccabees', '1 Mac', '1Maccabees', '1Macc'],
    ['2 Maccabees', '2 Mac', '2Maccabees', '2Macc'],
    ['3 Maccabees', '3 Mac', '3Maccabees', '3Macc'],
    ['4 Maccabees', '4 Mac', '4Maccabees', '4Macc'],
    ['Prayer of Manasseh', 'Manasseh']
];