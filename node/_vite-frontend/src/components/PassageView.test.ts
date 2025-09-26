import { PassageView } from "./PassageView.js";
import { Book } from "../models/Bible.js";
import type { IChapterResponse } from "../../../_shared/interfaces.js";


/**  Replace `PassageView.Generate` with `TEST__PassageView_Generate` to mutate incoming data to quickly test/observe PassageView with varying amount of columns.  
 *   Chapters 1-5, of any Book, will correspond to PassageView displaying 1-5 Columns for that chapter.
 *
 *   TESTING ENDPOINT: http://localhost:8080/?translations=KJV,NKJV,RSV,NRSV,NASB&book=Genesis&chapter=3
 */
export function TEST__PassageView_Generate(book:Book, chapter:number, data:IChapterResponse) {
    if(chapter === 1) {
        data.data.NASB = null;
        data.data.NRSV = null;
        data.data.RSV = null;
        data.data.NKJV = null;
        PassageView.Generate(book, chapter, data);
    }
    else if(chapter === 2) {
        data.data.NASB = null;
        data.data.NRSV = null;
        data.data.RSV = null;
        PassageView.Generate(book, chapter, data);
    }
    else if(chapter === 3) {
        data.data.NASB = null;
        data.data.NRSV = null;
        PassageView.Generate(book, chapter, data);
    }
    else if(chapter === 4) {
        data.data.NASB = null;
        PassageView.Generate(book, chapter, data);
    }
    else
        PassageView.Generate(book, chapter, data);
}