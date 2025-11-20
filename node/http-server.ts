import * as http from 'http';
import * as fs from 'fs';
import * as path from 'path'

import { print, printGreen } from './kozubenko/print.js';
import { Path } from './kozubenko/utils.js';
import { HtmlPage, handleNotFound } from './kozubenko/http.js';
import { GOOGLE_VM_EXTERNAL_IP } from './kozubenko/google.js';
import { ApiEndpoints } from './_shared/enums/ApiEndpoints.enum.js';
import { Api } from './api.js';



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


const DIST  = path.join(__dirname, '_vite-frontend', 'dist');
const PAGES = [
    new HtmlPage('/'       , path.join(DIST, 'index.html')),
    new HtmlPage('/report/', path.join(DIST, 'report.html'))
]

/**  Technically, this is meant to handle asset-like resource requests. eg: `index.js`/`index.css` requests after: `index.html`. */
function handleResourceRequest(pathname:string, response:http.ServerResponse): void {
    const requestedResource = Path.safeJoin(DIST, pathname);
    if(!fs.existsSync(requestedResource)) {
        handleNotFound(response);
        return;
    }
    
    fs.readFile(requestedResource, (error, data) => {
        if (error) {
            response.writeHead(404, { 'Content-Type': 'text/plain' });
            response.end(`Not Found: ${pathname}`);
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
    
    const url = new URL(request.url, `http://localhost:${PORT}`);             /* CHECK THIS LINE NEXT TIME YOU SPIN UP A GOOGLE VM: why does localhost work? */
    const page = PAGES.find(page => page.route === url.pathname);

    if(page)
        page.handle(response);

    else if(Object.values(ApiEndpoints).includes(url.pathname as ApiEndpoints))
        Api.Handle(url, response);

    else
        handleResourceRequest(url.pathname, response);
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