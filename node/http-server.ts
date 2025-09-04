import * as http from 'http';
import * as fs from 'fs';
import * as Path from 'path'

import { print, printGreen, printRed, printYellow } from './_shared/print.js';
import { handleNotFound, handleBadRequest } from './kozubenko/http.js';
import { combinePaths, safeSplit } from './kozubenko/utils.js';
import { BIBLE } from './models/Bible.js';
import { Status } from './_shared/enums.js';
import { performance } from "node:perf_hooks";

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
    
    const param1:string = URL.searchParams.get('translations') ?? '';
    const param2:string = URL.searchParams.get('book')    ?? '';
    const param3:string = URL.searchParams.get('chapter') ?? '';
    const param4:string = URL.searchParams.get('verses')  ?? '';

    if (!param2 || !param3) {  handleBadRequest(response); return;  }
    
    const translations: string[] = param1 ? param1.split(',').filter(translation => translation) : ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT'];
    if(translations.length < 1) {  handleBadRequest(response); return;  }
    
    const book = BIBLE.getBook(param2);
    if(!book) {  handleBadRequest(response); return;  }

    const chapterStart = parseInt(safeSplit(param3, "-")[0], 10)
    const chapterEnd   = parseInt(safeSplit(param3, "-")[1], 10)

    if(!chapterStart || chapterStart < 1 || chapterStart > book.chapters) {  handleBadRequest(response, `${book.name}:${chapterStart} is not a real Bible chapter.`); return;  }

    if(chapterEnd && chapterEnd > 1 && chapterEnd < book.chapters - 1) {
        if(chapterEnd - chapterStart > 1) {  handleBadRequest (response, `API does not support GET requests on >2 chapters.`); return;  }
    }

    
    const promises = await translations.map(async translation => {
        const chapterFile = Path.join(BIBLE_TXT, translation, book.name, `${chapterStart}.txt`);
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

server.listen(PORT, '0.0.0.0', () => {
    printGreen('Endpoints: ');
    if (PORT === DEV_PORT) {
        printGreen(`  http://${HOST}:${PORT}/`)
        printGreen(`  http://${HOST}:${PORT}/?book=Genesis&chapter=3&translations=KJV,NASB,RSV,RUSV,NKJV,ESV,NRSV,NRT`)
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


function GOOGLE_VM_EXTERNAL_IP() {
    return fetch(
        "http://169.254.169.254/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip", {
            headers: { "Metadata-Flavor": "Google" }
        }
    ).then(res => res.text());
}