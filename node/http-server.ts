import * as http from "node:http";
import * as fs from "node:fs";
import * as path from "node:path"

import { print } from "./kozubenko/print.ts";

print("process.argv", process.argv);
print("__dirname", __dirname);

const PORT = 8080;

const server = http.createServer((req, res) => {
    const INDEX_HTML = path.join(__dirname, "..", "frontend", "index.html");

    if (!req.url)   return;

    // GET /passage?book=Matthew&chapter=22&translation=NKJV;ESV

    const urlObj = new URL(req.url, `http://localhost:${PORT}`);
    if (urlObj.pathname === "/passage") {
        const translationString = urlObj.searchParams.get("translation") ?? "";

        const book = urlObj.searchParams.get("book") ?? "";
        const chapter = urlObj.searchParams.get("chapter") ?? "";
        const translations = translationString.split(";").filter(v => v);

        if 
    }

    fs.readFile(INDEX_HTML, (error, data) => {
        if (error) {
            res.writeHead(500, { "Content-Type": "text/html"});
            res.end("Error Loading: index.html");
            return;
        }

        res.writeHead(200, {"Content-Type": "text/html"});
        res.end(data);
    });
});


server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});