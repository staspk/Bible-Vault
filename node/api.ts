import * as fs from 'fs';
import * as path from 'path'
import * as http from 'http'

import { printRed, printYellow } from './kozubenko/print.js';
import { handleBadRequest, handleOK } from './kozubenko/http.js';
import { isNullOrWhitespace } from './kozubenko/string.extensions.js';
import { ApiEndpoints } from './_shared/ApiEndpoints.js';
import { BIBLE, Book } from './models/Bible.js';
import { BibleTranslations } from './_shared/BibleTranslations.js';
import { IVerseRange } from './_shared/interfaces/IVerseRange.js';
import { IChapter, IChapters, IReport } from './_shared/interfaces/IResponses.js';


const BIBLE_DIRECTORY = path.join(import.meta.dirname, '..', 'bible_txt');


export class Api {
    /** Assumes caller has checked `URL.pathname` with `ApiEndpoints.isEndpoints()` */
    static Handle(URL:URL, response:http.ServerResponse) {
        if (URL.pathname === ApiEndpoints.Bible)
            Bible.Handle(URL, response);
        if (URL.pathname === ApiEndpoints.Bible_Report)
            Bible_Report.Handle(URL, response);
    }
}

/** `/api/bible` */
class Bible {
    /**  `/api/bible?` -> `IChapterResponse` | `IChaptersResponse`  */
    static async Handle(URL:URL, response:http.ServerResponse) {
        printYellow(`API-Bible Request: ${URL.pathname}?${URL.searchParams.toString()}`);

        const param1:string = URL.searchParams.get('translations') ?? '';
        const param2:string = URL.searchParams.get('book')    ?? '';
        const param3:string = URL.searchParams.get('chapter') ?? '';        // potential forms: {int} || {int}-{int}
        const param4:string = URL.searchParams.get('verses')  ?? '';        // potential forms: {int} || {int}-{int}
        
        if (!param2 || !param3) {  handleBadRequest(response); return;  }
        
        const translations:string[] = param1 ? param1.split(',').filter(translation => translation) : ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT'];
        if(translations.length < 1 || translations.length > 10) {  handleBadRequest(response); return;  }

        const book = BIBLE.Book(param2);
        if(!book) {  handleBadRequest(response, 'Not a valid Bible Book'); return;  }
        
        const chapterStart = parseInt(param3.split("-")[0], 10);
        const chapterEnd   = parseInt(param3.split("-")[1], 10);
        
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
        
        if(!isNullOrWhitespace(param4)) {
            const verseStart = parseInt(param4.split("-")[0], 10);
            const verseEnd   = parseInt(param4.split("-")[1], 10);
            
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
        const promises = translations.map(async translation => {
            const file = path.join(BIBLE_DIRECTORY, translation, book.name, `${chapter}.txt`);
            if (!fs.existsSync(file))
                return { [translation.toUpperCase()]: null };
            
            return { [translation.toUpperCase()]: await Bible.loadChapterIntoMemory(file, verseRange) }
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

/** `/api/bible-report` */
class Bible_Report {
    static Handle(URL:URL, response:http.ServerResponse) {
        const param1:string = URL.searchParams.get('translations') ?? '';
        const translations:string[] = param1 ? param1.split(',').filter(translation => translation)
                                             : Object.values(BibleTranslations);

        let chapters:number[] = new Array(BIBLE.totalChapters()).fill(translations.length);
        chapters.forEach((chapter, i) => {
            translations.forEach(translation => {
                const ptr = BIBLE.ChaptersMap(i+1);
                const file = path.join(BIBLE_DIRECTORY, translation, ptr.book.name, `${ptr.chapter}.txt`);
                if (!fs.existsSync(file))
                    chapters[i]--;
            });
        });

        // printYellow(`API-Report Total Time: ${URL.pathname}`);
        handleOK(response, [...chapters] as IReport);
    }
}