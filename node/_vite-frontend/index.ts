import { isNullOrWhitespace, safeSplit } from '../kozubenko/string.extensions.js';
import { isUInt, yankUIntFromEnd } from './src/ts/utils';
import { IChapter, type IChapterResponse, type IChapters, type IChaptersResponse } from '../_shared/interfaces/IResponses.js';
import { BIBLE } from './src/models/Bible';
import { PassageView } from './src/components/PassageView/PassageView.js';

import './src/keyboard';
import './src/components/ReportBtn/ReportBtn.js';


class ContentView {
    static ID = 'content-view';

    static PlaceHolder(): HTMLDivElement {
        return document.querySelector(`#${ContentView.ID} :nth-child(2)`) as HTMLDivElement;
    }
}


const urlParams = new URLSearchParams(window.location.search);
const searchInput = document.getElementById('search-input') as HTMLInputElement;


const TRANSLATIONS = (urlParams.get('translations') ?? 'KJV,NASB,RSV,RUSV,NKJV,ESV,NRSV,NRT').split(',').filter(translation => translation) ;
const BOOK         = urlParams.get('book');
const CHAPTER      = urlParams.get('chapter');
const VERSES       = urlParams.get('verses');



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
            const response = await fetch(`/api/bible/?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}-${chapterEnd}`);
            if (response.status !== 200) return;
            
            const chapters:IChapters = (await response.json() as IChaptersResponse).data;
            
            PassageView.Render(ContentView.PlaceHolder(), chapterStart, IChapter.from(chapters, chapterStart));
            window.history.pushState({}, '', `?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}-${chapterEnd}`);
            /* SAVE the rest of the chapters locally, so don't have to ping server for next chapter */
            return;
        }
        
        
        if(!isNullOrWhitespace(potentialVerses)) {
            verseStart = safeSplit(potentialVerses, "-")[0];
            verseEnd   = safeSplit(potentialVerses, "-")[1];
            
            if(!isUInt(verseStart)) return;         /* decision: don't bother hitting the server, if the verses string is not legit  */
            
            QueryString = `?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}&verses=${verseStart}`;     /* searchStr shape: "Matthew 10:1"   */
            
            if(isUInt(verseEnd))
                QueryString += `-${verseEnd}`;                                                                                          /* searchStr shape: "Matthew 10:1-2" */
            
            const response = await fetch(`/api/bible/${QueryString}`);
            if (response.status !== 200) return;
            
            PassageView.Render(ContentView.PlaceHolder(), chapterStart, (await response.json() as IChapterResponse).data)
            window.history.pushState({}, '', QueryString);
            return;
        }
        
        // searchStr shape: "Matthew 10"
        const response = await fetch(`/api/bible/?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}`);
        if (response.status !== 200) return;
        
        PassageView.Render(ContentView.PlaceHolder(), chapterStart, (await response.json() as IChapterResponse).data);
        window.history.pushState({}, '', `?translations=${TRANSLATIONS.join(',')}&book=${book.name}&chapter=${chapterStart}`);
    }, 750);
});

if(BOOK && CHAPTER) {   /*  if urlParams, set page state */
    let searchStr = `${BOOK} ${CHAPTER}`;
    if(VERSES) {
        const verseStart = safeSplit(VERSES, "-")[0];
        const verseEnd   = safeSplit(VERSES, "-")[1];
        
        searchStr += `:${verseStart}`;
        if(verseEnd) searchStr += `-${verseEnd}`;
    }
    searchInput.value = searchStr;
    searchInput.dispatchEvent(new Event('input', { bubbles: true }));
}