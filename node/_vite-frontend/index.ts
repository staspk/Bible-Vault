import { Timer } from '../_shared/Timer.js';
import { print, yankUIntFromEnd } from './src/ts/utils.js';
import { BIBLE, Book } from '../_shared/Bible.js';
import type { IChapterResponse } from '../_shared/interfaces.js';

const urlParams = new URLSearchParams(window.location.search);

const BOOK         = urlParams.get('book');
const CHAPTER      = urlParams.get('chapter');
const TRANSLATIONS = (urlParams.get('translations') ?? 'KJV,NKJV,RSV,NRSV,NASB').split(',').filter(translation => translation);


const searchInput = document.getElementById('search-input') as HTMLInputElement;
if(BOOK && CHAPTER) searchInput.value = `${BOOK} ${CHAPTER}`;


function generatePassageDiv(book:Book, chapter:number, data:IChapterResponse) {
    const oldPassageDiv = document.getElementById('passage-div');
    const newPassageDiv = Object.assign(document.createElement('div'), {
        id: oldPassageDiv?.id
    });
    
    // const columns: Array<HTMLDivElement|null> = [];
    for (const [i, [translation, chapterMap]] of Object.entries(data.data).entries()) {
        if (chapterMap == null) continue;

        const chapterColumn = Object.assign(document.createElement('div'), {
            className: 'chapter-column',
            id: translation
        });
        
        for (const [verseNumber, verseText] of Object.entries(chapterMap)) {
            chapterColumn.append(Object.assign(document.createElement('div'), {
                id: `${translation}-${chapter}-${verseNumber}`,
                // class: `verse-${verseNumber}`,
                innerHTML: `<strong>${verseNumber}</strong> ${verseText}`
            }))
        }
        newPassageDiv.append(chapterColumn);
    }
    oldPassageDiv?.replaceWith(newPassageDiv);
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
        
        generatePassageDiv(book, chapter, await response.json());
    }, 750);
});