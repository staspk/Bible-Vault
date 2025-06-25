import * as http from "node:http";
import * as fs from "node:fs";
import * as path from "node:path"

import { print } from "./kozubenko/print.ts";

print("process.argv", process.argv)

const PORT = 8080;

const server = http.createServer((req, res) => {
    
});


server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});