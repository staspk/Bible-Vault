import * as http from 'http';
import * as fs from 'fs';
import * as Path from 'path'

import { print, printGreen, printRed, printYellow } from './_shared/print.js';
import { handleNotFound, handleBadRequest } from './kozubenko/http.js';
import { combinePaths } from './kozubenko/utils.js';
import { BIBLE } from './models/Bible.js';
import { Status } from './_shared/enums.js';

const __dirname = import.meta.dirname
print('process.argv', process.argv);
print()


const PORT = 8080;

const DIST       = Path.join(__dirname, '_vite-frontend', 'dist');
const BIBLE_TXT  = Path.join(__dirname, '..', 'bible_txt');
const INDEX_HTML = Path.join(DIST, 'index.html');

function handleResourceRequest(pathname:string, response:http.ServerResponse): void {
    const requestedResource = combinePaths(DIST, pathname);
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


/**
* Currently only one API endpoint:
* 
*   `/api/?book=Genesis&chapter=5&translations=KJV,NKJV,RSV,NRSV,NASB`  ***RETURNS***: `IChapterResponse`
*/
async function handleApiRequest(URL:URL, response:http.ServerResponse) {
    printYellow(`API Request: ${URL.pathname}?${URL.searchParams.toString()}`);
    
    const param1:string = URL.searchParams.get('book') ?? '';
    const param2:string = URL.searchParams.get('chapter') ?? '';
    const param3:string = URL.searchParams.get('translations') ?? 'KJV,NKJV,RSV,NRSV,NASB';
    
    if (!param1 || !param2) {  handleBadRequest(response); return;  }
    
    const book = BIBLE.getBook(param1);     // Stan: yes, you handle garbage input well, fyi
    const chapter = parseInt(param2, 10);   // Stan: yes, you handle garbage input well, fyi
    const translations: string[] = param3 ? param3.split(',').filter(translation => translation) : ['KJV', 'NKJV', 'RSV', 'NRSV', 'NASB'];  // Stan: well, fyi
    
    if (!book || !chapter || translations.length < 1) {  handleBadRequest(response); return;  }
    
    if (chapter < 1 || chapter > book.chapters) {  handleBadRequest(response, `${book.name}:${chapter} is not a real Bible chapter.`); return;  }
    
    const promises = await translations.map(async translation => {
        const chapterFile = Path.join(BIBLE_TXT, translation, book.name, `${chapter}.txt`);
        if (fs.existsSync(chapterFile))
            return { [translation.toUpperCase()]: await loadChapterIntoMemory(chapterFile) };
        
        return { [translation.toUpperCase()]: null };
    });
    
    const data = await Promise.all(promises);
    
    if (data.every(obj => Object.values(obj)[0] !== null)) {
        response.writeHead(200, { 'Content-Type': 'application/json' });
        response.end(JSON.stringify({
            status: Status.Success,
            data: Object.assign({}, ...data)
        }));
        return;
    } else if (data.every(obj => Object.values(obj)[0] === null)) {
        handleNotFound(response); return;
    } else {
        response.writeHead(200, { 'Content-Type': 'application/json' });
        response.end(JSON.stringify({
            status: Status.Partial,
            data: Object.assign({}, ...data)
        }));
    }
}

const server = http.createServer((request, response) => {
    if (!request.url) return;
    
    const urlObj = new URL(request.url, `http://localhost:${PORT}`);
    // printYellow(`CURRENT PATHNAME: ${urlObj.pathname}`);
    if (urlObj.pathname === '/') {
        fs.readFile(INDEX_HTML, (error, data) => {
            if (error) {
                response.writeHead(500, { 'Content-Type': 'text/html'});
                response.end('Error Loading: index.html');
                return;
            }
            response.writeHead(200, {'Content-Type': 'text/html'});
            response.end(data);
        });
        return;
    }
    
    else if (urlObj.pathname === '/api/')
        handleApiRequest(urlObj, response);
    
    else
    handleResourceRequest(urlObj.pathname, response);
});

server.listen(PORT, () => {
    printGreen('Endpoints: ');
    printGreen(`  http://localhost:${PORT}/`)
    printGreen(`  http://localhost:${PORT}/?book=Genesis&chapter=3&translations=KJV,NKJV,RSV,NRSV,NASB`)
});



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