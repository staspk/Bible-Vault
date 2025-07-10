import { print, yankUIntFromEnd } from './src/ts/utils.js';
import { BIBLE, Book } from '../_shared/Bible.js';
import type { IChapterResponse } from '../_shared/interfaces.js';


const urlParams = new URLSearchParams(window.location.search);
const searchInput = document.getElementById('search-input') as HTMLInputElement;

const BOOK         = urlParams.get('book');
const CHAPTER      = urlParams.get('chapter');
const TRANSLATIONS = (urlParams.get('translations') ?? 'KJV,NKJV,RSV,NRSV,NASB').split(',').filter(translation => translation);

if (BOOK && CHAPTER)
    searchInput.value = `${BOOK} ${CHAPTER}`;


function generatePassageDiv(book:Book, chapter:number, data:IChapterResponse) {
    const columns: HTMLDivElement[] = [];
    for (const [i, [translation, chapterMap]] of Object.entries(data.data).entries()) {
        if (!chapterMap)
            continue;

        columns[i] = Object.assign(document.createElement('div'), {
            className: 'chapter-column',
            id: translation
        });
        for (const [verseNumber, verseText] of Object.entries(chapterMap)) {
            columns[i].append(Object.assign(document.createElement('div'), {
                id: `${verseNumber}`,
                innerHTML: `<strong>${verseNumber}</strong> ${verseText}`
            }))
        }
    }
    return columns;
}

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

        const data: IChapterResponse = await response.json();

        console.log(data)
        
        // createPassageDiv(data.data);


        
    }, 750);
});

if (BOOK && CHAPTER)
    searchInput.value = `${BOOK} ${CHAPTER}`;


for (let translation of TRANSLATIONS) {
    
}