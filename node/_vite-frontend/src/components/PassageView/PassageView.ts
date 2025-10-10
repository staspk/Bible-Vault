
import './PassageView.scss';
import { IChapter } from "../../../../_shared/interfaces/IResponses";
import { LocalStorage } from '../../storage/LocalStorage';
import { LocalStorageKeys } from '../../storage/LocalStorageKeys.enum';
import { isNullOrUndefined } from '../../../../kozubenko/utils';


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
    static mirrorOption = LocalStorage.getBoolean(LocalStorageKeys.mirrorOption);

    static view1: HTMLDivElement;
    static view2?: HTMLDivElement;
    static currentView: View = View.None;

    /**  Renders `PassageView`, splitting between 1-2 views, depending on `mirrorOption` and `data`.  
        Only 1-10 translations per `chapter` supported.  */
    static Render(ONTO:HTMLElement, chapter:number, data:IChapter) {
        if(isNullOrUndefined(ONTO)) {
            console.error('PassageView.Render(): ONTO is null/undefined. Cannot complete Render!');
            return;
        }

        ONTO.id = PassageView.ID;

        let total_translations = 0, view1_translations = 0, view2_translations = 0;
        for (const [i, [key, value]] of Object.entries(data).entries())
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

        PassageView.view1 = PassageView.generateView(chapter, view1_translations, IChapter.range(0, view1_translations, data));
        if(PassageView.view2) delete PassageView.view2;
        if(view2_translations > 0)
            PassageView.view2 = PassageView.generateView(chapter, view2_translations, IChapter.range(view1_translations, (view1_translations+view2_translations), data));

        
        ONTO.replaceWith(PassageView.view1);
        PassageView.currentView = View.One;
        PassageView.alignVerses();
    }
    
    /** A `PassageView` `view` holds 1-5 translations of the same chapter. */
    static generateView(chapter:number, total_translations:number, data:IChapter): HTMLDivElement {
        const view = Object.assign(document.createElement('div'), {
            id: PassageView.ID
        });
        
        view.classList.add(COLUMNS_CLASS(total_translations));
        
        for (const [i, [translation, chapterMap]] of Object.entries(data).entries()) {
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
        let passageView = document.getElementById(PassageView.ID) as HTMLDivElement;
        if(!passageView) {
            console.error('PassageView.alignVerses(): PassageView could not be found via PassageView.ID. Skipping function...');
            return;
        }
        
        let row = 1;
        let nodes = passageView.querySelectorAll(`.row-${row}`) as NodeListOf<HTMLDivElement>;
        while (nodes.length > 0) {
            let minHeight = Math.max(...Array.from(nodes, node => node.clientHeight));
            nodes.forEach((node) => {
                node.style.minHeight = minHeight + "px";
            });
            row++;
            nodes = passageView.querySelectorAll(`.row-${row}`)
        }
    }
    
    /**  Toggles between `PassageView.view1` and  `PassageView.view2`, depending on: `PassageView.currentView`  */
    static toggleView() {
        if(PassageView.currentView === View.None) {
            console.error('PassageView.toggleView(): cannot be called before PassageView.Render(), ie: PassageView.currentView === View.None. Skipping Function...');
            return;
        }
        
        const passageView = document.getElementById(PassageView.ID);
        if(!passageView) {
            console.error('PassageView.toggleView(): PassageView could not be found via PassageView.ID. Skipping function...');
            return;
        }
        
        if(PassageView.currentView === View.One) {
            if(PassageView.view2) {
                passageView.replaceWith(PassageView.view2);
                PassageView.alignVerses();
                PassageView.currentView = View.Two;
                return;
            }
        }
        
        if(PassageView.currentView === View.Two) {
            passageView.replaceWith(PassageView.view1);
            PassageView.alignVerses();
            PassageView.currentView = View.One;
            return;
        }
    }
}