import { Timer } from '../_shared/Timer';
import { isUInt, print, safeSplit, yankUIntFromEnd } from './src/ts/utils';
import { BIBLE, Book } from './src/models/Bible';
import { printGreen, printRed, printYellow } from '../_shared/print';
import type { IChapterResponse } from '../_shared/interfaces';
import { PassageDiv } from './src/components/PassageDiv';
import { isNullOrWhitespace } from '../kozubenko/utils';


const urlParams = new URLSearchParams(window.location.search);
const searchInput = document.getElementById('search-input') as HTMLInputElement;


const TRANSLATIONS = (urlParams.get('translations') ?? 'KJV,NASB,RSV,RUSV,NKJV,ESV,NRSV,NRT').split(',').filter(translation => translation) ;
const BOOK         = urlParams.get('book');
const CHAPTER      = urlParams.get('chapter');
const VERSES       = urlParams.get('verses')


let searchDebounceTimerID;
searchInput.addEventListener('input', (event) => {
    clearTimeout(searchDebounceTimerID);

    const searchStr = (event.target as HTMLInputElement).value.trim();
    if (!searchStr) return;
    
    searchDebounceTimerID = setTimeout(async () => {
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
            const response = await fetch(`/api/?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}-${chapterEnd}`);
            if (response.status !== 200) return;

            PassageDiv.Generate(book, chapterStart, await response.json() as IChapterResponse);
            window.history.pushState({}, '', `?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}-${chapterEnd}`);
            return;
        }

        if(!isNullOrWhitespace(potentialVerses)) {
            verseStart = safeSplit(potentialVerses, "-")[0];
            verseEnd   = safeSplit(potentialVerses, "-")[1];

            if(isUInt(verseStart)) {
                QueryString = `/api/?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}&verses=${verseStart}`;

                if(isUInt(verseEnd))
                    QueryString += `-${verseEnd}`;

                const response = await fetch(QueryString);
                if (response.status !== 200) return;

                PassageDiv.Generate(book, chapterStart, await response.json() as IChapterResponse)
                // PassageDiv.Test.Generate(book, chapterStart, await response.json() as IChapterResponse);
                window.history.pushState({}, '', `?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}&verses=${verseStart}`);
                return;
            }
        }

        // e.g: "Matthew 10"
        const response = await fetch(`/api/?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}`);
        if (response.status !== 200) return;

        PassageDiv.Generate(book, chapterStart, await response.json() as IChapterResponse);
        window.history.pushState({}, '', `?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}`);
    }, 750);
});


if(BOOK && CHAPTER) {
    searchInput.value = `${BOOK} ${CHAPTER}`;
    searchInput.dispatchEvent(new Event('input', { bubbles: true }));
}
