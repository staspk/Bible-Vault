import { Timer } from './ts/Timer.js';
import { print, yankUIntFromEnd } from './ts/utils.js';
import { BIBLE, BIBLE_SEARCH_TERMS } from './ts/Bible.js';

const urlParams = new URLSearchParams(window.location.search);
const searchInput = document.getElementById('search-input') as HTMLInputElement;


const BOOK         = urlParams.get('book');
const CHAPTER      = urlParams.get('chapter');
const TRANSLATIONS = (urlParams.get('translations') ?? 'KJV,NKJV,RSV,NRSV,NASB').split(',').filter(translation => translation);

let searchDebounceTimerID;

searchInput.addEventListener('input', (event) => {
    clearTimeout(searchDebounceTimerID);
    
    const searchStr = (event.target as HTMLInputElement).value.trim();
    if (!searchStr) return;
    
    searchDebounceTimerID = setTimeout(async () => {
        const result = yankUIntFromEnd(searchStr);
        if (!result[0]) return;

        const book = BIBLE.searchBook(result[1].trim());
        if (!book) return;

        if (result[0] < 0 || result[0] > book.chapters) return;

        const response = await fetch(`/api/?book=${book.name}&chapter=${result[0]}&translations=${TRANSLATIONS.join(',')}`);
        if (response.status !== 200) return;
        
        const data = await response.json();
        console.log('Search results:', data);
            
    }, 750);
});

if (BOOK && CHAPTER)
    searchInput.value = `${BOOK} ${CHAPTER}`;


for (let translation of TRANSLATIONS) {
    
}