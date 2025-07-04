import * as http from 'http';
import * as fs from 'fs';
import * as path from 'path'

import { print, printGreen, printRed, printYellow } from './kozubenko/print';
import { combinePaths } from './kozubenko/utils';
import { BIBLE } from './models/Bible';


print('process.argv', process.argv);
print()

const PORT = 8080;

const INDEX_HTML = path.join(__dirname, 'vite-frontend', 'dist', 'index.html');
const DIST       = path.join(__dirname, 'vite-frontend', 'dist');

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
        printYellow(`API Request: ${urlObj.pathname}`);
        
        const param1: string = urlObj.searchParams.get('book') ?? '';
        const param2: string = urlObj.searchParams.get('chapter') ?? '';
        const param3: string = urlObj.searchParams.get('translations') ?? '';
        
        const book = BIBLE.getBook(param1);
        const chapter = parseInt(param2, 10);
        const translations = param3.split(';').filter(translation => translation);
        
        if (!book || !chapter || translations.length < 0) {
            response.writeHead(400, { 'Content-Type': 'application/json' });
            response.end(JSON.stringify({ error: 'Missing required query params' }));
            return;
        }
    }

    else
        handleResourceRequest(urlObj.pathname, response);
});


server.listen(PORT, () => {
    printGreen('Endpoints: ');
    printGreen(`  http://localhost:${PORT}/`)
    printGreen(`  http://localhost:${PORT}/?book=Genesis&chapter=3&translations=KJV;NKJV;RSV;NRSV;NASB`)
});