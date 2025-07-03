import { Timer } from './ts/Timer.js';
import { print } from './ts/utils.js';
import { BIBLE, BIBLE_SEARCH_TERMS } from './ts/Bible.js';

const urlParams = new URLSearchParams(window.location.search);
const searchInput = document.getElementById('search-input');


const book         = urlParams.get('book');
const chapter      = urlParams.get('chapter');
const translations = (urlParams.get('translations') ?? '').split(';').filter(translation => translation);

let searchDebounceTimerID;

searchInput.addEventListener('input', (event) => {
    clearTimeout(searchDebounceTimerID);
    
    const searchStr = event.target.value.trim();
    if (!searchStr) return;
    
    searchDebounceTimerID = setTimeout(async () => {
        print('searchStr', searchStr)
        // Timer.start()
        if(!BIBLE_SEARCH_TERMS.includes(searchStr)) return;

        searchstr
        // Timer.stop()


        try {
            const response = await fetch(`/api/?book=${book}&chapter=${chapter}&translations=${translations}`);
            if (!response.ok) throw new Error('index.js: Network Error');
            
            const data = await response.json();
            console.log('Search results:', data);
            
        } catch (error) {
            console.error()
        }
    }, 750);
});

if (book && chapter)
    searchInput.value = `${book} ${chapter}`;


for (translation in translations) {
    
}