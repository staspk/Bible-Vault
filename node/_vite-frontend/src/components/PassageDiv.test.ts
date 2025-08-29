import { PassageDiv } from "./PassageDiv.js";
import { Book } from "../models/Bible.js";
import type { IChapterResponse } from "../../../_shared/interfaces.js";


/**
 * TESTING ENDPOINT: http://localhost:8080/?translations=KJV,NKJV,RSV,NRSV,NASB&book=Genesis&chapter=3
 * 
 * Observe/test `PassageDiv` various grid layouts (1-5 columns, corresponding to chapters 1-5 of any Book). 
*/
export function TEST__PassageDiv_Generate(book:Book, chapter:number, data:IChapterResponse) {
    if(chapter === 1) {
        data.data.NASB = null;
        data.data.NRSV = null;
        data.data.RSV = null;
        data.data.NKJV = null;
        PassageDiv.Generate(book, chapter, data);
    }
    else if(chapter === 2) {
        data.data.NASB = null;
        data.data.NRSV = null;
        data.data.RSV = null;
        PassageDiv.Generate(book, chapter, data);
    }
    else if(chapter === 3) {
        data.data.NASB = null;
        data.data.NRSV = null;
        PassageDiv.Generate(book, chapter, data);
    }
    else if(chapter === 4) {
        data.data.NASB = null;
        PassageDiv.Generate(book, chapter, data);
    }
    else
        PassageDiv.Generate(book, chapter, data);
}