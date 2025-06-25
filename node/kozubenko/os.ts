import * as fs from 'fs';
import * as Path from 'path';

/**
 * Returns a path string your OS needs. Creates the directory (including parent dirs) if it doesn't exist.
 */
function Directory(path: string, ...paths: string[]): string {
    const dir = Path.join(path, ...paths);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    return dir;
}