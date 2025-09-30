
import './PassageView.scss';
import { Book } from "../models/Bible";
import { IResponses, type IChapterResponse } from "../../../_shared/interfaces"
import { LocalStorage, LocalStorageKeys } from '../localStorage';


/**  A pre-defined CSS class is picked, determining `width` and `grid-template-columns` *[`PassageView.scss`]*  */
const COLUMNS_CLASS = (total_translations:number) => `cols-${total_translations}`;

enum View {
    None = 'none',
    One  = 'view1',
    Two  = 'view2'
}

/**  `#passage-view`: consists of 1-2 `views` [grid of 1-5 columns/translations of a Bible chapter].  */
export class PassageView {
    static ID = 'passage-view';
    
    /** when true: even amount of translations are halved between 2 views. */
    static mirrorOption = LocalStorage.getBoolean(LocalStorageKeys.mirrorOption)

    static view1: HTMLDivElement;
    static view2: HTMLDivElement;
    static currentView: View = View.None;
    
    /**  Generates and mounts onto: `document.getElementById(PassageView.ID)`  
        Only 1-10 translations per chapter supported  */
    static Generate(book:Book, chapter:number, data:IChapterResponse) {
        const PLACEHOLDER = document.getElementById(PassageView.ID);
        if(!PLACEHOLDER) {
            console.error('PassageView.Generate(): PLACEHOLDER could not be found via PassageView.ID. Skipping function...');
            return;
        }
        
        let total_translations = 0, view1_translations = 0, view2_translations = 0;
        for (const [i, [key, value]] of Object.entries(data.data).entries())
            total_translations++;
        
        if(PassageView.mirrorOption && (total_translations % 2 === 0)) {
            view1_translations = total_translations / 2;
            view2_translations = total_translations / 2;
        } else {
            if(total_translations > 5) {
                view1_translations = 5;
                view2_translations = total_translations - 5;
            } else
                view1_translations = total_translations;
        }

        PassageView.view1 = PassageView.generateView(chapter, view1_translations, IResponses.range(0, view1_translations, data));
        if(view2_translations > 0)
            PassageView.view2 = PassageView.generateView(chapter, view2_translations, IResponses.range(view1_translations, (view1_translations+view2_translations), data));
        
        PLACEHOLDER.replaceWith(PassageView.view1);
        PassageView.currentView = View.One;
        PassageView.alignVerses();
    }
    
    /** A `PassageView` `view` holds 1-5 translations of the same chapter. */
    static generateView(chapter:number, total_translations:number, data:IChapterResponse): HTMLDivElement {
        const view = Object.assign(document.createElement('div'), {
            id: PassageView.ID
        });
        
        view.classList.add(COLUMNS_CLASS(total_translations));
        
        for (const [i, [translation, chapterMap]] of Object.entries(data.data).entries()) {
            if (chapterMap == null) continue;   /* If a chap is missing, the translation tables don't match when mirrorOption==true. Need to design an empty column */
            
            const chapterColumn = Object.assign(document.createElement('div'), {
                className: 'chapter-column',
                id: translation
            });
            
            let row = 1;
            for (const [verseNumber, verseText] of Object.entries(chapterMap)) {
                chapterColumn.append(Object.assign(document.createElement('div'), {
                    id: `${translation}-${chapter}-${verseNumber}`,
                    className: `row-${row}`,
                    innerHTML: verseNumber === '1'
                    ? `<span class="chapter-dropcap">${chapter}</span> ${verseText}`
                    : `<span class="versenum">${verseNumber}</span> ${verseText}`
                }))
                row++;
            }
            view.append(chapterColumn);
        }
        
        return view;
    }
    
    /**  Helper function. Should be called after the `view` has been placed into the DOM.  
    * Iterates over Columns/Translations, aligning same verses between translations to start at the same y position.  */
    static alignVerses() {
        let PASSAGE_DIV = document.getElementById(PassageView.ID) as HTMLDivElement;
        if(!PASSAGE_DIV) {
            console.error('PassageView.alignVerses(): PASSAGE_DIV could not be found via PassageView.ID. Skipping function...');
            return;
        }
        
        let row = 1;
        let nodes = PASSAGE_DIV.querySelectorAll(`.row-${row}`) as NodeListOf<HTMLDivElement>;
        while (nodes.length > 0) {
            let minHeight = Math.max(...Array.from(nodes, node => node.clientHeight));
            nodes.forEach((node) => {
                node.style.minHeight = minHeight + "px";
            });
            row++;
            nodes = PASSAGE_DIV.querySelectorAll(`.row-${row}`)
        }
    }
    
    /**  Toggles between `PassageView.view1` and  `PassageView.view2`, depending on: `PassageView.currentView`  */
    static toggleView() {
        if(PassageView.currentView === View.None) {
            console.error('PassageView.toggleView(): called incorrectly [PassageView.currentView === View.None]. Skipping Function...');
            return;
        }
        
        const PLACEHOLDER = document.getElementById(PassageView.ID);
        if(!PLACEHOLDER) {
            console.error('PassageView.toggleView(): PLACEHOLDER could not find via PassageView.ID. Skipping function...');
            return;
        }
        
        if(PassageView.currentView === View.One) {
            PLACEHOLDER.replaceWith(PassageView.view2);
            PassageView.alignVerses();
            PassageView.currentView = View.Two;
            return;
        }
        
        if(PassageView.currentView === View.Two) {
            PLACEHOLDER.replaceWith(PassageView.view1);
            PassageView.alignVerses();
            PassageView.currentView = View.One;
            return;
        }
    }
}