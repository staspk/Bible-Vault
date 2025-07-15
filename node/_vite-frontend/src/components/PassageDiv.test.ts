import { generatePassageDiv } from "./PassageDiv";
import { Book } from "../../../_shared/Bible";
import type { IChapterResponse } from "../../../_shared/interfaces";

/**
*  TESTING ENDPOINT: http://localhost:8080/?book=Genesis&chapter=3&translations=KJV,NKJV,RSV,NRSV,NASB
*   to test: replace generatePassageDiv() calls with TEST_generatePassageDiv()
* 
*   Fakes data, so chapters 1-5 (corresponds to columns 1-5) of any Book can be used to observe/test grid column layouts of #passage-div
*/
export function TEST_generatePassageDiv(book:Book, chapter:number, data:IChapterResponse) {
    if(chapter === 1) {
        data.data.NASB = null;
        data.data.NRSV = null;
        data.data.RSV = null;
        data.data.NKJV = null;
        generatePassageDiv(book, chapter, data);
    }
    else if(chapter === 2) {
        data.data.NASB = null;
        data.data.NRSV = null;
        data.data.RSV = null;
        generatePassageDiv(book, chapter, data);
    }
    else if(chapter === 3) {
        data.data.NASB = null;
        data.data.NRSV = null;
        generatePassageDiv(book, chapter, data);
    }
    else if(chapter === 4) {
        data.data.NASB = null;
        generatePassageDiv(book, chapter, data);
    }
    else
        generatePassageDiv(book, chapter, data);
}