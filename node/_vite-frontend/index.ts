import { safeSplit } from '../kozubenko/string.extensions';
import { SearchInput } from './src/components/SearchInput/SearchInput';
import { LocalStorageKeys } from './src/storage/LocalStorageKeys.enum';
import { LocalStorage } from './src/storage/LocalStorage.js';

import './src/storage/LocalStorage.js'
import './src/keyboard.js';
import './src/components/HomeBtn/HomeBtn.js'
import './src/components/ReportBtn/ReportBtn.js';
import './src/components/SearchInput/SearchInput.js'


export class ContentView {
    static ID = 'content-view';
    
    static PlaceHolder(): HTMLDivElement {
        return document.querySelector(`#${ContentView.ID} :nth-child(2)`) as HTMLDivElement;
    }
}


const urlParams = new URLSearchParams(window.location.search);
export const TRANSLATIONS = urlParams.get('translations')?.split(',').filter(el => el) ?? LocalStorage.getArray(LocalStorageKeys.TRANSLATIONS);
export const BOOK         = urlParams.get('book');
export const CHAPTER      = urlParams.get('chapter');
export const VERSES       = urlParams.get('verses');

if(BOOK && CHAPTER) {
    let searchStr = `${BOOK} ${CHAPTER}`;
    if(VERSES) {
        const verseStart = safeSplit(VERSES, "-")[0];
        const verseEnd   = safeSplit(VERSES, "-")[1];
        
        searchStr += `:${verseStart}`;
        if(verseEnd) searchStr += `-${verseEnd}`;
    }
    SearchInput.Set(searchStr);
}