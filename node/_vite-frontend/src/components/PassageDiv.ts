import { BIBLE, Book } from "../models/Bible";
import type { IChapterResponse, IChaptersResponse } from "../../../_shared/interfaces"
import { printGreen, printYellow } from "../../../_shared/print";
import { Timer } from "../../../_shared/Timer";


/** CSS class that's used to determine `width` and `grid-template-columns` for: `#passage-div` */
const COLUMNS_CLASS = (total_translations:number) => `cols-${total_translations}`;

export class PassageDiv {
    static ID = 'passage-div';

    static mirrorOption = true;    /*  when true: 6,8 translations are halved between 2 tables. */

    /**  Generates and mounts onto `PassageDiv.PLACEHOLDER` [`#passage-div`]  
     *   Only 1-10 translations per chapter supported  */
    static Generate(book:Book, chapter:number, data:IChapterResponse) {
        const PLACEHOLDER = document.getElementById(PassageDiv.ID);
        let passageDiv = Object.assign(document.createElement('div'), {
            id: PLACEHOLDER?.id
        });

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

        passageDiv.classList.add(COLUMNS_CLASS(view1_translations))
        passageDiv = PassageDiv.constructPassageView(passageDiv, chapter, view1_translations, data);
        
        PLACEHOLDER?.replaceWith(passageDiv);
        
        PassageDiv.alignVerses();
    }

    static constructPassageView(passageDiv:HTMLDivElement, chapter:number, total_columns:number, data:IChapterResponse): HTMLDivElement {
        // const columns: Array<HTMLDivElement|null> = [];
        for (const [i, [translation, chapterMap]] of Object.entries(data.data).entries()) {
            if(i < total_columns) {
                if (chapterMap == null) continue;   /* If a chap is missing, the translation tables don't match when >5 translations. <=5, don't match COLUMNS_CLASS. Need to design an empty column */
                
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
                passageDiv.append(chapterColumn);
            }
        }
        return passageDiv;
    }

    /**  Helper function to `PassageDiv.Generate()`. Aligns rows so that equal verses between translations start at the same y position.  */
    static alignVerses() {
        const PASSAGE_DIV = document.getElementById(PassageDiv.ID) as HTMLDivElement;
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