import * as fs from 'fs';
import * as path from 'path'
import * as http from 'http'

import { printRed, printYellow } from './kozubenko/print.js';
import { handleBadRequest, handleOK } from './kozubenko/http.js';
import { isNullOrWhitespace, safeSplit } from './kozubenko/string.extensions.js';
import { BIBLE, Book } from './models/Bible.js';
import { IChapter, IChapters } from './_shared/interfaces/IResponses.js';
import { IVerseRange } from './_shared/interfaces/IVerseRange.js';
import { ApiEndpoints } from './_shared/enums/ApiEndpoints.enum.js';


export class Api {

    /** Assumes caller has checked if `URL.pathname` is an `ApiEndpoints.enum` */
    static Handle(URL:URL, response:http.ServerResponse) {
        if (URL.pathname === ApiEndpoints.Bible)
            Bible.Handle(URL, response);
        if (URL.pathname === ApiEndpoints.Report)
            Report.Handle(URL, response);
    }
}

/** `/api/bible` */
class Bible {

    static BIBLE_TXT = path.join(import.meta.dirname, '..', 'bible_txt');

    /**  `/api/bible?` -> `IChapterResponse` | `IChaptersResponse`  */
    static async Handle(URL:URL, response:http.ServerResponse) {
        printYellow(`API Request: ${URL.pathname}?${URL.searchParams.toString()}`);
            
        const param1:string = URL.searchParams.get('translations') ?? '';
        const param2:string = URL.searchParams.get('book')    ?? '';
        const param3:string = URL.searchParams.get('chapter') ?? '';
        const param4:string = URL.searchParams.get('verses')  ?? '';
        
        if (!param2 || !param3) {  handleBadRequest(response); return;  }
        
        const translations: string[] = param1 ? param1.split(',').filter(translation => translation) : ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT'];
        if(translations.length < 1 || translations.length > 10) {  handleBadRequest(response); return;  }
        
        const book = BIBLE.getBook(param2);
        if(!book) {  handleBadRequest(response); return;  }
        
        const chapterStart = parseInt(safeSplit(param3, "-")[0], 10);
        const chapterEnd   = parseInt(safeSplit(param3, "-")[1], 10);
        
        if(!chapterStart || chapterStart < 1 || chapterStart > book.chapters) {  handleBadRequest(response, `${book.name}:${chapterStart} is not a real Bible chapter.`); return;  }
        
        if(chapterEnd && chapterEnd > 1 && chapterEnd < book.chapters + 1) {    /*  multiple chapters call. See: _shared/IChaptersResponse  */
            if(chapterEnd - chapterStart > 1) {  handleBadRequest(response, `API does not support GET requests on >2 chapters`); return;  }
            
            let chapters: IChapters = {
                [chapterStart]: await Bible.getChapter(translations, book, chapterStart),
                [chapterEnd]  : await Bible.getChapter(translations, book, chapterEnd)
            }
    
            handleOK(response, IChapters.wrapAsResponse(chapters));
            return;
        }
        
        if(!isNullOrWhitespace(param4)) {   /*  */
            const verseStart = parseInt(safeSplit(param4, "-")[0], 10);
            const verseEnd   = parseInt(safeSplit(param4, "-")[1], 10);
            
            if(verseStart && verseStart > 0 && (verseStart <= 89 || (verseStart <= 176 && book === BIBLE.PSALMS)) ) {   /* verseStart must be 1-89 || 1-176 (if: Psalms) */
                if(verseEnd && verseEnd > 1 && (verseEnd <= 89   || (verseEnd   <= 176 && book === BIBLE.PSALMS)) ) {   /* verseEnd   must be 2-89 || 2-176 (if: Psalms) */
                    if(verseStart < verseEnd) {
                        /* Legit Multiple Verses Api Call, ie: "Matthew 10:11-12" */
                        let chapter: IChapter = await Bible.getChapter(translations, book, chapterStart, { verseStart: verseStart, verseEnd: verseEnd } as IVerseRange);
                        handleOK(response, IChapter.wrapAsResponse(chapter)); return;
                    } else {
                        handleBadRequest(response, `GET API Call requested non-existent verse or malformed verse range.`); return;
                    }
                }
                /* Targetted Single Verse Api Call, ie: "Matthew 10:11" */
                let chapter: IChapter = await Bible.getChapter(translations, book, chapterStart, { verseStart: verseStart, verseEnd: verseStart } as IVerseRange);
                handleOK(response, IChapter.wrapAsResponse(chapter)); return;
            }
            handleBadRequest(response, `GET API Call requested non-existent verse or malformed verse range.`);
            return;
        }
        
        /* Standard API Call, ie: "Matthew 10" */
        let chapter: IChapter = await Bible.getChapter(translations, book, chapterStart);
        handleOK(response, IChapter.wrapAsResponse(chapter));
    }

    static async getChapter(translations:string[], book:Book, chapter:number, verseRange:IVerseRange|null=null): Promise<IChapter> {
        const promises = await translations.map(async translation => {
            const chapterFile = path.join(Bible.BIBLE_TXT, translation, book.name, `${chapter}.txt`);
            if (!fs.existsSync(chapterFile))
                return { [translation.toUpperCase()]: null };
            
            return { [translation.toUpperCase()]: await Bible.loadChapterIntoMemory(chapterFile, verseRange) }
        });

        return Object.assign({}, ...await Promise.all(promises));
    }

    /**
    * Assumption: each line in the file maps to one verse.
    *
    * @returns Plain object (aka: dict) mapping verse numbers to verse text, or null on error.
    * @example
    * {
    *   "1": "In the beginning God created the heavens and the earth.",
    *   "2": "And the earth was without form, and void; and darkness was upon the face of the deep.",
    *   "3": "And the Spirit of God moved upon the face of the waters."
    * }
    */
    static async loadChapterIntoMemory(path:string, verseRange:IVerseRange|null=null): Promise<object|null> { 
        try {
            const data = await fs.promises.readFile(path, 'utf-8');
            const lines = data.split(/\r?\n/);
            const plainObj = Object.fromEntries(
                lines.map((line, i) => [ (i + 1).toString(), line ])
            );

            if(verseRange)
                for (const [key, value] of Object.entries(plainObj))
                    if (parseInt(key) < verseRange.verseStart || parseInt(key) > verseRange.verseEnd)
                        delete plainObj[key];
            
            return plainObj;
            
        } catch (error) {
            printRed(`loadChapterIntoMemory(${path}): ${error}`);
            return null;
        }
    }
}

/** /api/report */
class Report {
    static Handle(URL:URL, response:http.ServerResponse) {
        printYellow(`API Request: ${URL.pathname}`);

        handleOK(response, {});
    }
}