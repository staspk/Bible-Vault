import * as http from 'http';
import * as fs from 'fs';
import * as Path from 'path'

import { print, printGreen, printRed, printYellow } from './_shared/print.js';
import { handleNotFound, handleBadRequest } from './kozubenko/http.js';
import { combinePaths, safeSplit } from './kozubenko/utils.js';
import { BIBLE, Book } from './models/Bible.js';
import { Status } from './_shared/enums.js';
import { performance } from "node:perf_hooks";
import { GOOGLE_VM_EXTERNAL_IP } from './kozubenko/google.js';

const __dirname = import.meta.dirname
print('process.argv', process.argv);
print()



const DIST         = Path.join(__dirname, '_vite-frontend', 'dist');
const BIBLE_TXT    = Path.join(__dirname, '..', 'bible_txt');
const INDEX_HTML   = Path.join(DIST, 'index.html');
const TRANSLATIONS = ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT']


let chapterStart = await getChapter(BIBLE.GENESIS, 1, TRANSLATIONS);
let chapterEnd   = await getChapter(BIBLE.GENESIS, 2, TRANSLATIONS);

let chapters = chapterStart.concat(chapterEnd)

console.log(chapters)


/**
* @returns Plain object (aka: dict) mapping verse numbers to verse text, or null on error.
* @example
* {
*   "1": "In the beginning God created the heavens and the earth.",
*   "2": "And the earth was without form, and void; and darkness was upon the face of the deep.",
*   "3": "And the Spirit of God moved upon the face of the waters."
* }
*/
async function getChapter(book:Book, chapter:number, translations:string[]): Promise<object[]> {
    const promises = await translations.map(async translation => {
        const chapterFile = Path.join(BIBLE_TXT, translation, book.name, `${chapter}.txt`);
        if (!fs.existsSync(chapterFile))
            return { [translation.toUpperCase()]: null };

        return { [translation.toUpperCase()]: await loadChapterIntoMemory(chapterFile) };
    });

    return await Promise.all(promises);
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
async function loadChapterIntoMemory(path:string): Promise<object|null> { 
    try {
        const data = await fs.promises.readFile(path, 'utf-8');
        const lines = data.split(/\r?\n/);
        return Object.fromEntries(
            lines.map((line, i) => [ (i + 1).toString(), line ])
        );
    } catch (error) {
        printRed(`loadChapterIntoMemory(): ${error}`);
        return null;
    }
}