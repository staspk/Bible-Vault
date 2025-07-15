import { Timer } from '../_shared/Timer';
import { print, yankUIntFromEnd } from './src/ts/utils';
import { BIBLE, Book } from '../_shared/Bible';
import { printRed } from '../_shared/print';
import type { IChapterResponse } from '../_shared/interfaces';
import { TEST_generatePassageDiv } from './src/components/PassageDiv.test';
import { generatePassageDiv } from './src/components/PassageDiv';


const searchInput = document.getElementById('search-input') as HTMLInputElement;
let searchDebounceTimerID;
searchInput.addEventListener('input', (event) => {
    clearTimeout(searchDebounceTimerID);
    
    const searchStr = (event.target as HTMLInputElement).value.trim();
    if (!searchStr) return;
    
    searchDebounceTimerID = setTimeout(async () => {
        const [int, string] = yankUIntFromEnd(searchStr);
        if (!int) return;
        
        const book    = BIBLE.searchBook(string.trim());
        const chapter = int;
        
        if (!book) return;
        if (chapter < 0 || chapter > book.chapters) return;
        
        const response = await fetch(`/api/?book=${book.name}&chapter=${chapter}&translations=${TRANSLATIONS.join(',')}`);
        if (response.status !== 200) return;

        generatePassageDiv(book, chapter, await response.json() as IChapterResponse);
    }, 750);
});


const urlParams = new URLSearchParams(window.location.search);

const BOOK         = urlParams.get('book');
const CHAPTER      = urlParams.get('chapter');
const TRANSLATIONS = (urlParams.get('translations') ?? 'KJV,NKJV,RSV,NRSV,NASB').split(',').filter(translation => translation);

if(BOOK && CHAPTER) {
    searchInput.value = `${BOOK} ${CHAPTER}`;
    searchInput.dispatchEvent(new Event('input', { bubbles: true }));
}

