import * as http from 'http';
import * as fs from 'fs';
import * as path from 'path'

import { print, printGreen, printYellow } from './kozubenko/print';
import { BIBLE } from './models/Bible';

print('process.argv', process.argv);
print()

const PORT = 8080;

const INDEX_HTML = path.join(__dirname, '..', 'frontend', 'index.html');
const INDEX_JS   = path.join(__dirname, '..', 'frontend', 'index.js');
const INDEX_CSS  = path.join(__dirname, '..', 'frontend', 'index.css');

const server = http.createServer((request, response) => {
    if (!request.url) {
        return
    }

    const urlObj = new URL(request.url, `http://localhost:${PORT}`);
    if (urlObj.pathname === '/') {                                               // GET /passage?book=Matthew&chapter=22&translation=NKJV;ESV
        const param1: string = urlObj.searchParams.get('book') ?? '';
        const param2: string = urlObj.searchParams.get('chapter') ?? '';
        const param3: string = urlObj.searchParams.get('translation') ?? '';

        const book = BIBLE.getBook(param1);
        const chapter = parseInt(param2, 10);
        const translations = param3.split(';').filter(translation => translation);

        if (!book || !chapter || translations.length < 0) {
            response.writeHead(400, { 'Content-Type': 'application/json' });
            response.end(JSON.stringify({ error: 'Missing required query params' }));
            return;
        }
        
        fs.readFile(INDEX_HTML, (error, data) => {
            if (error) {
                response.writeHead(500, { 'Content-Type': 'text/html'});
                response.end('Error Loading: index.html');
                return;
            }

            response.writeHead(200, {'Content-Type': 'text/html'});
            response.end(data);
        });
    }
    if (urlObj.pathname === '/index.js') {
        fs.readFile(INDEX_JS, (error, data) => {
            if (error) {
                response.writeHead(404, { 'Content-Type': 'text/plain' });
                response.end('Not Found: index.js');
                return;
            }
            response.writeHead(200, { 'Content-Type': 'application/javascript' });
            response.end(data);
        });
    }
    if (urlObj.pathname === '/index.css') {
        fs.readFile(INDEX_CSS, (error, data) => {
            if (error) {
                response.writeHead(404, { 'Content-Type': 'text/plain' });
                response.end('Not Found: index.css');
                return;
            }
            response.writeHead(200, { 'Content-Type': 'text/css' });
            response.end(data);
        });
    }

    if (urlObj.pathname === '/api/') {
    const param1: string = urlObj.searchParams.get('book') ?? '';
    const param2: string = urlObj.searchParams.get('chapter') ?? '';
    const param3: string = urlObj.searchParams.get('translation') ?? '';

    const book = BIBLE.getBook(param1);
    const chapter = parseInt(param2, 10);
    const translations = param3.split(';').filter(translation => translation);

    if (!book || !chapter || translations.length < 0) {
        response.writeHead(400, { 'Content-Type': 'application/json' });
        response.end(JSON.stringify({ error: 'Missing required query params' }));
        return;
    }
});


server.listen(PORT, () => {
    printGreen('Endpoints: ');
    printGreen(`  http://localhost:${PORT}/`)
    printGreen(`  http://localhost:${PORT}/passage?book=Genesis&chapter=3&translations=KJV;NKJV;RSV;NRSV;NASB`)
});