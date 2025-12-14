import './src/storage/LocalStorage.js';
import './src/keyboard.js';
import './src/services/Router.js';
import './src/components/HomeBtn/HomeBtn.js';
import './src/components/ReportBtn/ReportBtn.js';
import './src/components/SearchInput/SearchInput.js';
import { Document } from './kozubenko.ts/Document.js';
import { Router } from './src/services/Router.js';
import { SearchInput } from './src/components/SearchInput/SearchInput.js';



export class ContentView {
    static ID = 'content-view';

    static Reset() {
        document.title = "BIBLE";
        SearchInput.Reset();
        this.PlaceHolder().replaceWith(Document('div', {id: 'content-view-placeholder'}));
    }
    
    static PlaceHolder(): HTMLDivElement {
        return document.querySelector(`#${ContentView.ID} :nth-child(2)`) as HTMLDivElement;
    }
}


new Router();