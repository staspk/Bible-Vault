/* 
    Some Test Results:

    "Matthew 10".split(":")[0] => returns "Matthew 10"
    "Matthew 10".split(":")[1] => returns undefined
*/
import { IChapterResponse } from "../_shared/interfaces.js";
import { printGreen, printRed, printYellow } from "../_shared/print.js"
import { isNullOrWhitespace } from "../kozubenko/utils.js"
import { generatePassageDiv } from "./src/components/PassageDiv.js";
import { BIBLE } from "./src/models/Bible.js";
import { isUInt, safeSplit, yankUIntFromEnd } from "./src/ts/utils.js"


const TRANSLATIONS = ('KJV,NKJV,RSV,NRSV,NASB').split(',').filter(translation => translation);

async function mockedParseSearchStringAndFetch(searchStr:string) {
    const potentialBookChapter = safeSplit(searchStr, ":")[0];
    const potentialVerses      = safeSplit(searchStr, ":")[1];

    if(isNullOrWhitespace(potentialBookChapter)) return;

    let book, chapterStart, chapterEnd, verseStart, verseEnd, QueryString;

    const [uint, potentialBook] = yankUIntFromEnd(safeSplit(potentialBookChapter, "-")[0]);
    if (!uint) return;
    
    book         = BIBLE.searchBook(potentialBook.trim());
    chapterStart = uint;
    chapterEnd   = safeSplit(potentialBookChapter, "-")[1]
    
    if (!book) return;
    if (chapterStart < 0 || chapterStart > book.chapters) return;

    if(isUInt(chapterEnd)) {    // e.g: "Matthew 10-11" (does not support verses)
        // const response = await fetch(`/api/?book=${book.name}&chapter=${chapterStart}-${chapterEnd}&translations=${TRANSLATIONS.join(',')}`);
        // if (response.status !== 200) return;

        // generatePassageDiv(book, chapterStart, await response.json() as IChapterResponse);
        // return;
        printGreen(`fetching: api/?book=${book.name}&chapter=${chapterStart}-${chapterEnd}&translations=${TRANSLATIONS.join(',')}`);
        return;
    }

    if(!isNullOrWhitespace(potentialVerses)) {
        verseStart = safeSplit(potentialVerses, "-")[0];
        verseEnd   = safeSplit(potentialVerses, "-")[1];

        if(isUInt(verseStart)) {
            QueryString = `/api/?book=${book.name}&chapter=${chapterStart}&translations=${TRANSLATIONS.join(',')}&verses=${verseStart}`;

            if(isUInt(verseEnd))
                QueryString += `-${verseEnd}`;

            printGreen(`fetching: ${QueryString}`);

            // const response = await fetch(QueryString);
            // if (response.status !== 200) return;

            // generatePassageDiv(book, chapterStart, await response.json() as IChapterResponse);
            return;
        }
    }

    // e.g: "Matthew 10"
    // const response = await fetch(`/api/?book=${book.name}&chapter=${chapterStart}&translations=${TRANSLATIONS.join(',')}`);
    // if (response.status !== 200) return;

    // generatePassageDiv(book, chapterStart, await response.json() as IChapterResponse);

    printGreen(`/api/?book=${book.name}&chapter=${chapterStart}&translations=${TRANSLATIONS.join(',')}`)
}


mockedParseSearchStringAndFetch("Matthew 10:12")
