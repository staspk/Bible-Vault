import * as http from 'http';
import * as fs from 'fs';
import * as Path from 'path'
import { fileURLToPath } from 'url';

import { print, printGreen, printRed, printYellow } from './kozubenko/print.js';
import { handleNotFound, respondBadRequest, Status } from './kozubenko/http.js';
import { combinePaths } from './kozubenko/utils.js';
import { BIBLE, Book } from './models/Bible.js';

const __dirname = import.meta.dirname
print('process.argv', process.argv);
print()


const PORT = 8080;

const INDEX_HTML = Path.join(__dirname, 'vite-frontend', 'dist', 'index.html');
const DIST       = Path.join(__dirname, 'vite-frontend', 'dist');
const BIBLE_TXT  = Path.join(__dirname, '..', 'bible_txt');

function handleResourceRequest(pathname:string, response:http.ServerResponse): void {
    const requestedResource = combinePaths(DIST, pathname);
    if(!fs.existsSync(requestedResource)) {
        response.writeHead(204, { 'Content-Type': 'text/plain' });              // 204 - No Content
        response.end();
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
 * @returns 
 */
async function loadChapterIntoMemory(path:string): Promise<object|null> { 
    try {
        const data = await fs.promises.readFile(path, 'utf-8');
        const lines = data.split(/\r?\n/);
        
        // Use 1-based indexing
        return Object.fromEntries(
            lines.map((line, i) => [ (i + 1).toString(), line ])
        );
    } catch (error) {
        printRed(`readChapter(): ${error}`);
        return null;
    }
}

/**
* Tests using the data: array object's value of the 1'st property
* data { 'nkjv': null, 'rsv': `${data}` }
*
*/
function checkStatus(data): Status {
    
    if(data.every(obj => Object.values(obj)[0] !== null))
        return Status.Success;
        return Status.Error;
    return Status.Partial;
}

const server = http.createServer((request, response) => {
    if (!request.url) return;
    
    const urlObj = new URL(request.url, `http://localhost:${PORT}`);
    // printYellow(`CURRENT PATHNAME: ${urlObj.pathname}`);
    if (urlObj.pathname === '/') {                                               // GET /?book=Matthew&chapter=22&translation=NKJV;ESV 
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

    else if (urlObj.pathname === '/api/') {
        printYellow(`API Request: ${urlObj.pathname}?${urlObj.searchParams.toString()}`);
        
        const param1:string = urlObj.searchParams.get('book') ?? '';
        const param2:string = urlObj.searchParams.get('chapter') ?? '';
        const param3:string = urlObj.searchParams.get('translations') ?? 'KJV,NKJV,RSV,NRSV,NASB';
        
        if (!param1 || !param2) {  respondBadRequest(response); return;  }
        
        const book = BIBLE.getBook(param1);     // Stan: yes, you handle garbage input ahead with a falsy check
        const chapter = parseInt(param2, 10);   // Stan: yes, you handle garbage input ahead with a falsy check
        const translations: string[] = param3 ? param3.split(',').filter(translation => translation) : ['KJV', 'NKJV', 'RSV', 'NRSV', 'NASB'];  // Stan: garbage rejected on testpath
        
        if (!book || !chapter || translations.length < 1) {  respondBadRequest(response); return;  }
        
        if (chapter < 1 || chapter > book.chapters) {  respondBadRequest(response, `${book.name}:${chapter} is not a real Bible chapter.`); return;  }
        
        (async () => {
            const promises = translations.map(async translation => {
                const chapterFile = Path.join(BIBLE_TXT, translation, book.name, `${chapter}.txt`);
                if (fs.existsSync(chapterFile))
                    // return await loadChapterIntoMemory(chapterFile);
                    return { [translation.toUpperCase()]: await loadChapterIntoMemory(chapterFile) };
                
                return { [translation.toUpperCase()]: null };
            });
            
            const data = await Promise.all(promises);

            if (data.every(obj => Object.values(obj)[0] !== null)) {
                response.writeHead(200, { 'Content-Type': 'application/json' });
                response.end(JSON.stringify({
                    status: Status.Success,
                    data: data,
                }));
                return;
            } else if (data.every(obj => Object.values(obj)[0] === null)) {
                handleNotFound(response); return;
            } else {
                response.writeHead(200, { 'Content-Type': 'application/json' });
                response.end(JSON.stringify({
                    status: Status.Success,
                    data: Object.assign({}, ...data)
                }));
            }
        })();
    }

    else
        handleResourceRequest(urlObj.pathname, response);
});


server.listen(PORT, () => {
    printGreen('Endpoints: ');
    printGreen(`  http://localhost:${PORT}/`)
    printGreen(`  http://localhost:${PORT}/?book=Genesis&chapter=3&translations=KJV,NKJV,RSV,NRSV,NASB`)
});