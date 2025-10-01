import { isNullOrWhitespace, safeSplit } from '../kozubenko/string.extensions.js';
import { isUInt, yankUIntFromEnd } from './src/ts/utils';
import { IResponses, type IChapterResponse, type IChaptersResponse } from '../_shared/interfaces/IResponses.js';
import { BIBLE } from './src/models/Bible';
import { PassageView } from './src/components/PassageView';

import './src/keyboard';


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
        chapterEnd   = safeSplit(potentialBookChapter, "-")[1];
        
        if (!book) return;
        if (chapterStart < 0 || chapterStart > book.chapters) return;
        
        if(isUInt(chapterEnd)) {    /* searchStr shape: "Matthew 10-11" [IChaptersResponse (does not support verses)] */
            const response = await fetch(`/api/?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}-${chapterEnd}`);
            if (response.status !== 200) return;
            
            PassageView.Generate(book, chapterStart, IResponses.transform(chapterStart, await response.json() as IChaptersResponse));
            window.history.pushState({}, '', `?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}-${chapterEnd}`);
            /* SAVE chapterEnd local, so don't have to ping server for next chapter */
            return;
        }
        

        if(!isNullOrWhitespace(potentialVerses)) {
            verseStart = safeSplit(potentialVerses, "-")[0];
            verseEnd   = safeSplit(potentialVerses, "-")[1];
            
            if(!isUInt(verseStart)) return;         /* decision: don't bother hitting the server, if the verses string is not legit  */

            QueryString = `/api/?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}&verses=${verseStart}`;    /* searchStr shape: "Matthew 10:1"   */
            
            if(isUInt(verseEnd))
                QueryString += `-${verseEnd}`;                                                                                              /* searchStr shape: "Matthew 10:1-2" */
            
            const response = await fetch(QueryString);
            if (response.status !== 200) return;
            
            PassageView.Generate(book, chapterStart, await response.json() as IChapterResponse)
            window.history.pushState({}, '', `?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}&verses=${verseStart}`);
            return;
        }
        
        // searchStr shape: "Matthew 10"
        const response = await fetch(`/api/?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}`);
        if (response.status !== 200) return;
        
        PassageView.Generate(book, chapterStart, await response.json() as IChapterResponse);
        window.history.pushState({}, '', `?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}`);
    }, 750);
});


if(BOOK && CHAPTER) {   /*  if urlParams, set page state */
    searchInput.value = `${BOOK} ${CHAPTER}`;
    searchInput.dispatchEvent(new Event('input', { bubbles: true }));
}