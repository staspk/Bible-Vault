import { Timer } from './js/Timer.js';
import { BIBLE, BIBLE_SEARCH_TERMS } from './js/Bible.js';

const urlParams = new URLSearchParams(window.location.search);
const searchInput = document.getElementById('search-input');


const book         = urlParams.get('book');
const chapter      = urlParams.get('chapter');
const translations = (urlParams.get('translations') ?? '').split(';').filter(translation => translation);

let searchDebounceTimerID;

searchInput.addEventListener('input', (event) => {
    clearTimeout(searchDebounceTimerID);
    
    const value = event.target.value.trim();
    if (!value) return;
    
    searchDebounceTimerID = setTimeout(async () => {
        Timer.start()
        BIBLE_SEARCH_TERMS.includes(value)
        Timer.stop() 


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