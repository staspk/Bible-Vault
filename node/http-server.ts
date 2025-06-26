import * as http from 'http';
import * as fs from 'fs';
import * as path from 'path'

import { print, printGreen } from './kozubenko/print';
import { BIBLE, BibleReference, Book } from './models/Bible';
import { assert_class } from './kozubenko/typing';

print('process.argv', process.argv);
print('__dirname', __dirname);
print('testing-number', 10)

const PORT = 8080;

const server = http.createServer((req, res) => {
    const INDEX_HTML = path.join(__dirname, '..', 'frontend', 'index.html');

    if (!req.url) { return }

    

    const urlObj = new URL(req.url, `http://localhost:${PORT}`);
    if (urlObj.pathname === '/passage') {                                               // GET /passage?book=Matthew&chapter=22&translation=NKJV;ESV
        const param1: string = urlObj.searchParams.get('book') ?? '';
        const param2: string = urlObj.searchParams.get('chapter') ?? '';
        const param3: string = urlObj.searchParams.get('translation') ?? '';
        
        const book = BIBLE.getBook(param1);
        const chapter = parseInt(param2, 10);
        const translations = param3.split(';').filter(translation => translation);

        let errorMessage = 'Error fetching from API';
            errorMessage += `book:`

        if (!book || !chapter || translations.length < 0) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Missing required query params' }));
            return;
        }

    }

    fs.readFile(INDEX_HTML, (error, data) => {
        if (error) {
            res.writeHead(500, { 'Content-Type': 'text/html'});
            res.end('Error Loading: index.html');
            return;
        }

        res.writeHead(200, {'Content-Type': 'text/html'});
        res.end(data);
    });
});


server.listen(PORT, () => {
    printGreen(`Server Serving! Try: http://localhost:${PORT}/passage?book=Genesis&chapter=3&translations=KJV;NKJV;RSV;NRSV;NASB`);
});