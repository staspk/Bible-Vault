import { PassageView } from "./PassageView.js";
import { Book } from "../../../../_shared/Bible.js";
import type { IChapter, IChapterResponse } from "../../../../_shared/interfaces/IResponses.js";


/**  Replace `PassageView.Generate` with `TEST__PassageView_Generate` to mutate incoming data to quickly test/observe PassageView with varying amount of columns.  
 *   Chapters 1-5, of any Book, will correspond to PassageView displaying 1-5 Columns for that chapter.
 *
 *   TESTING ENDPOINT: http://localhost:8080/?translations=KJV,NKJV,RSV,NRSV,NASB&book=Genesis&chapter=3
 */
export function TEST__PassageView_Generate(book:Book, chapter:number, data:IChapter) {
    if(chapter === 1) {
        data.NASB = null;
        data.NRSV = null;
        data.RSV = null;
        data.NKJV = null;
        PassageView.Generate(book, chapter, data);
    }
    else if(chapter === 2) {
        data.NASB = null;
        data.NRSV = null;
        data.RSV = null;
        PassageView.Generate(book, chapter, data);
    }
    else if(chapter === 3) {
        data.NASB = null;
        data.NRSV = null;
        PassageView.Generate(book, chapter, data);
    }
    else if(chapter === 4) {
        data.NASB = null;
        PassageView.Generate(book, chapter, data);
    }
    else
        PassageView.Generate(book, chapter, data);
}