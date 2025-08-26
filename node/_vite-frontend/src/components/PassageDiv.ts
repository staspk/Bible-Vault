import { BIBLE, Book } from "../models/Bible";
import type { IChapterResponse } from "../../../_shared/interfaces"
import { printGreen, printYellow } from "../../../_shared/print";
import { Timer } from "../../../_shared/Timer";

/** CSS class that's used to determine `width` and `grid-template-columns` for  `#passage-div` */
const COLUMNS_CLASS = (num_of_cols) => `cols-${num_of_cols}`;

/**  Generates html and also mounts onto the placeholder (`#passage-div`)  */
export function generatePassageDiv(book:Book, chapter:number, data:IChapterResponse) {
    const PLACEHOLDER = document.getElementById('passage-div');
    const passageDiv = Object.assign(document.createElement('div'), {
        id: PLACEHOLDER?.id
    });
    
    let total_translations = 0;
    for (const [i, [key, value]] of Object.entries(data.data).entries())
        if (value !== null)
            total_translations++;
    
    passageDiv.classList.add(COLUMNS_CLASS(total_translations))
    
    // const columns: Array<HTMLDivElement|null> = [];
    for (const [i, [translation, chapterMap]] of Object.entries(data.data).entries()) {
        if (chapterMap == null) continue;
        
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
    PLACEHOLDER?.replaceWith(passageDiv);
    alignRowsPassageDiv(book, chapter);
}

/**  Aligns rows so all verses from all translations start at the same y position. Call after #passage-div has been generated and injected into dom.  */
export function alignRowsPassageDiv(book:Book, chapter:number) {
    const PASSAGE_DIV = document.getElementById('passage-div') as HTMLDivElement;
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