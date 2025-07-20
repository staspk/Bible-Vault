import { BIBLE, Book } from "../../../_shared/Bible";
import type { IChapterResponse } from "../../../_shared/interfaces"

/** CSS class that's used to determine `width` and `grid-template-columns` for  `#passage-div` */
const COLUMNS_CLASS = (num_of_cols) => `cols-${num_of_cols}`;

/**  #passage-div  */
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
        for (const [verseNumber, verseText] of Object.entries(chapterMap)) {
            chapterColumn.append(Object.assign(document.createElement('div'), {
                id: `${translation}-${chapter}-${verseNumber}`,
                innerHTML: verseNumber === '1'
                ? `<span class="chapter-dropcap">${chapter}</span> ${verseText}`
                : `<span class="versenum">${verseNumber}</span> ${verseText}`
            }))
        }
        passageDiv.append(chapterColumn);
    }
    PLACEHOLDER?.replaceWith(passageDiv);
}