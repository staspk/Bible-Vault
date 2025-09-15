import { Book } from "../models/Bible";
import { IResponses, type IChapterResponse } from "../../../_shared/interfaces"


/** CSS class that's used to determine `width` and `grid-template-columns` for: `#passage-div` */
const COLUMNS_CLASS = (total_translations:number) => `cols-${total_translations}`;

export class PassageDiv {
    static ID = 'passage-div';

    static mirrorOption = true;    /*  when true: 6,8 translations are halved between 2 views. */

    static view1: HTMLDivElement;
    static view2: HTMLDivElement;

    /**  Generates and mounts onto `PassageDiv.PLACEHOLDER` [`#passage-div`]  
     *   Only 1-10 translations per chapter supported  */
    static Generate(book:Book, chapter:number, data:IChapterResponse) {
        const PLACEHOLDER = document.getElementById(PassageDiv.ID);
        if(!PLACEHOLDER) {
            console.error('PassageDiv.Generate() could not complete because document.getElementById({PassageDiv.ID}) failed...');
            return;
        }

        let total_translations = 0, view1_translations = 0, view2_translations = 0;
        for (const [i, [key, value]] of Object.entries(data.data).entries())
            total_translations++;

        if(PassageDiv.mirrorOption && (total_translations === 6 || total_translations === 8)) {
            view1_translations = total_translations / 2;
            view2_translations = total_translations / 2;
        } else {
            if(total_translations > 5) {
                view1_translations = 5;
                view2_translations = total_translations - 5;
            } else 
                view1_translations = total_translations;
        }

        PassageDiv.view1 = PassageDiv.generateView(chapter, view1_translations, IResponses.range(0, view1_translations, data));
        if(view2_translations > 0)
            PassageDiv.view2 = PassageDiv.generateView(chapter, view2_translations, IResponses.range(view1_translations-1, (view1_translations+view2_translations), data));

        PLACEHOLDER.replaceWith(PassageDiv.view1);
        PassageDiv.alignVerses();
    }

    static generateView(chapter:number, total_translations:number, data:IChapterResponse): HTMLDivElement {
        const view = Object.assign(document.createElement('div'), {
            id: PassageDiv.ID
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

    /**  Helper function to `PassageDiv.Generate()`. Aligns rows so that equal verses between translations start at the same y position.  */
    static alignVerses(div:any=null) {
        let PASSAGE_DIV = document.getElementById(PassageDiv.ID) as HTMLDivElement;

        if(div) {
            PASSAGE_DIV = div;
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
}