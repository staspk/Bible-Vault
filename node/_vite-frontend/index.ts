import { safeSplit } from '../kozubenko/string.extensions';
import { BibleSearch, Search } from './src/services/Search';
import { SearchInput } from './src/components/SearchInput/SearchInput';
import { LocalStorageKeys } from './src/storage/LocalStorageKeys.enum';
import { LocalStorage } from './src/storage/LocalStorage.js';

import './src/storage/LocalStorage.js'
import './src/keyboard.js';
import './src/components/ReportBtn/ReportBtn.js';
import './src/components/SearchInput/SearchInput.js'
import { BibleApi } from './src/services/api.js';
import { ApiEndpoints } from '../_shared/enums/ApiEndpoints.enum.js';
import { type IChapterResponse } from '../_shared/interfaces/IResponses.js';
import { PassageView } from './src/components/PassageView/PassageView.js';



export class ContentView {
    static ID = 'content-view';
    
    static PlaceHolder(): HTMLDivElement {
        return document.querySelector(`#${ContentView.ID} :nth-child(2)`) as HTMLDivElement;
    }
}


const urlParams = new URLSearchParams(window.location.search);
const searchInput = document.getElementById(SearchInput.ID) as HTMLInputElement;


const TRANSLATIONS = urlParams.get('translations')?.split(',').filter(el => el) ?? LocalStorage.getArray(LocalStorageKeys.TRANSLATIONS);
const BOOK         = urlParams.get('book');
const CHAPTER      = urlParams.get('chapter');
const VERSES       = urlParams.get('verses');


let searchDebounceTimerID;
searchInput.addEventListener('input', (event) => {
    clearTimeout(searchDebounceTimerID);
    
    const searchStr = (event.target as HTMLInputElement).value.trim();
    if (!searchStr) return;
    
    searchDebounceTimerID = setTimeout(async () => {
        const search = new Search(searchStr);

        if(search.data instanceof BibleSearch) {
            const queryString = BibleApi.From(search.data, TRANSLATIONS as string[]).queryString();

            const response = await fetch(`${ApiEndpoints.Bible}${queryString}`);
            if (response.status !== 200) return;

            PassageView.Render(ContentView.PlaceHolder(), search.data.chapter, (await response.json() as IChapterResponse).data);
            window.history.pushState({}, '', queryString);
            
            /*  DO ICHAPTERS LATER  */
        }        
    });
});


if(BOOK && CHAPTER) {   /*  if urlParams, set page state */
    let searchStr = `${BOOK} ${CHAPTER}`;
    if(VERSES) {
        const verseStart = safeSplit(VERSES, "-")[0];
        const verseEnd   = safeSplit(VERSES, "-")[1];
        
        searchStr += `:${verseStart}`;
        if(verseEnd) searchStr += `-${verseEnd}`;
    }
    SearchInput.Set(searchStr);
}