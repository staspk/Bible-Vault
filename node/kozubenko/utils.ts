
/**
 * Combines paths together (handles paths with forward `/`, backslashes `\`, or both)
 *
 * @returns {string} Returns a path with forward slashes `/`
 */
export function combinePaths(...paths: string[]): string {
    return paths
        .flatMap(path => path.split(/[\\/]/))
        .join('/');
}

export function isNullOrWhitespace(str:string): boolean {
    if(str == null || str.trim() === "")
        return true;
    return false;
}