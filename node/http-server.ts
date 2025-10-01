import * as http from 'http';
import * as fs from 'fs';
import * as Path from 'path'

import { print, printGreen, printRed, printYellow } from './_shared/print.js';
import { isNullOrWhitespace, safeSplit } from './kozubenko/string.extensions.js';
import { Paths } from './kozubenko/utils.js';
import { HtmlPage, handleOK, handleNotFound, handleBadRequest } from './kozubenko/http.js';
import { BIBLE, Book } from './models/Bible.js';
import { Status } from './_shared/enums.js';
import { IChapter, IChapters } from './_shared/interfaces/IResponses.js';
import { type IVerseRange } from './_shared/interfaces/IVerseRange.js'
import { GOOGLE_VM_EXTERNAL_IP } from './kozubenko/google.js';



const __dirname = import.meta.dirname
print('process.argv', process.argv);
print()


/**
* Ports under 1024 privileged on unix systems. Temporarily using: "sudo setcap 'cap_net_bind_service=+ep' $(which node)".
* Eventually: use Nginx/Apache as a reverse-proxy server on ports 80/443 and forward requests to your Node.js app on 8080.
*/
const HTTP_PORT  = 80;
const HTTPS_PORT = 443;
const DEV_PORT   = 8080;

const HOST:string = process.platform === 'linux' ? await GOOGLE_VM_EXTERNAL_IP() : '127.0.0.1';
const PORT:number = process.platform === 'linux' ? HTTP_PORT                     :  DEV_PORT;


const DIST       = Path.join(__dirname, '_vite-frontend', 'dist');
const BIBLE_TXT  = Path.join(__dirname, '..', 'bible_txt');
const PAGES = [
    new HtmlPage('/'      , Path.join(DIST, 'index.html')),
    new HtmlPage('/report', Path.join(DIST, 'report.html'))
]


/**  Technically, this is meant to handle asset-like resource requests. ie: `index.js`/`index.css` requests after being served `index.html`. */
function handleResourceRequest(pathname:string, response:http.ServerResponse): void {
    const requestedResource = Paths.safeJoin(DIST, pathname);
    if(!fs.existsSync(requestedResource)) {
        handleNotFound(response);
        return;
    }
    
    fs.readFile(requestedResource, (error, data) => {
        if (error) {
            response.writeHead(404, { 'Content-Type': 'text/plain' });
            response.end(`Not Found: ${pathname.substring}`);
            return;
        }
        
        if (pathname.split('.')[1].toLowerCase() === 'html')
            response.writeHead(200, {'Content-Type': 'text/html'});
        
        if (pathname.split('.')[1].toLowerCase() === 'js')
            response.writeHead(200, { 'Content-Type': 'application/javascript' });
        
        if (pathname.split('.')[1].toLowerCase() === 'css')
            response.writeHead(200, { 'Content-Type': 'text/css' });
        
        response.end(data);
    });
}


/**  `/api/bible?` => `IChapterResponse` | `IChaptersResponse`  */
async function handleApiRequest(URL:URL, response:http.ServerResponse) {
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
            [chapterStart]: await getChapter(translations, book, chapterStart),
            [chapterEnd]  : await getChapter(translations, book, chapterEnd)
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
                    let chapter: IChapter = await getChapter(translations, book, chapterStart, { verseStart: verseStart, verseEnd: verseEnd } as IVerseRange);
                    handleOK(response, IChapter.wrapAsResponse(chapter)); return;
                } else {
                    handleBadRequest(response, `GET API Call requested non-existent verse or malformed verse range.`); return;
                }
            }
            /* Targetted Single Verse Api Call, ie: "Matthew 10:11" */
            let chapter: IChapter = await getChapter(translations, book, chapterStart, { verseStart: verseStart, verseEnd: verseStart } as IVerseRange);
            handleOK(response, IChapter.wrapAsResponse(chapter)); return;
        }
        handleBadRequest(response, `GET API Call requested non-existent verse or malformed verse range.`);
        return;
    }
    
    /* Standard API Call, ie: "Matthew 10" */
    let chapter: IChapter = await getChapter(translations, book, chapterStart);
    handleOK(response, IChapter.wrapAsResponse(chapter));
}

const server = http.createServer((request, response) => {
    if (!request.url) return;
    
    const urlObj = new URL(request.url, `http://localhost:${PORT}`);             /* CHECK THIS LINE NEXT TIME YOU SPIN UP A GOOGLE VM: why does localhost work? */
    const page = PAGES.find(page => page.route === urlObj.pathname);

    if(page)
        page.handle(response);
    
    else if (urlObj.pathname === '/api/bible/')
        handleApiRequest(urlObj, response);
    else
        handleResourceRequest(urlObj.pathname, response);
});

server.listen(PORT, '0.0.0.0', () => {
    printGreen('Endpoints: ');
    if (PORT === DEV_PORT) {
        printGreen(`  http://${HOST}:${PORT}/`)
        printGreen(`  http://${HOST}:${PORT}/report`)
        printGreen(`  http://${HOST}:${PORT}/?book=Luke&chapter=21&verses19-21`)
        printGreen(`  http://${HOST}:${PORT}/?book=Genesis&chapter=3&translations=KJV,NASB,RSV,RUSV,NKJV,ESV,NRSV,NRT,NIV,NET`)
        // printGreen(`  http://${HOST}:${PORT}/?book=Genesis&chapter=3&translations=KJV,NASB,RSV,RUSV,NKJV,ESV,NRSV,NRT`)
        // printGreen(`  http://${HOST}:${PORT}/?book=Genesis&chapter=3&translations=KJV,NASB,RSV,NKJV,ESV`)
    }
    else if (PORT === HTTP_PORT) {
        printGreen(`  http://${HOST}/`)
        printGreen(`  http://${HOST}/?book=Genesis&chapter=3&translations=KJV,NASB,RSV,RUSV,NKJV,ESV,NRSV,NRT`)
    }
    else if (PORT === HTTPS_PORT) {
        printGreen(`  https://${HOST}/`)
        printGreen(`  https://${HOST}/?book=Genesis&chapter=3&translations=KJV,NASB,RSV,RUSV,NKJV,ESV,NRSV,NRT`)
    }
});




async function getChapter(translations:string[], book:Book, chapter:number, verseRange:IVerseRange|null=null): Promise<IChapter> {
    const promises = await translations.map(async translation => {
        const chapterFile = Path.join(BIBLE_TXT, translation, book.name, `${chapter}.txt`);
        if (!fs.existsSync(chapterFile))
            return { [translation.toUpperCase()]: null };
        
        return { [translation.toUpperCase()]: await loadChapterIntoMemory(chapterFile, verseRange) }
    });

    return Object.assign({}, ...await Promise.all(promises));                                    /* shape: IChapter    */
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
async function loadChapterIntoMemory(path:string, verseRange:IVerseRange|null=null): Promise<object|null> { 
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

// const chapter: IChapter = await getChapter(['KJV', 'NASB'], BIBLE.GENESIS, 1);

// console.log(IChapter.wrapAsResponse(chapter))