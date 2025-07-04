
/**
 * Combines paths together (handles paths with forward `/`, backslashes `\`, and both)
 *
 * @returns {string} Returns a path with forward slashes `/`
 */
export function combinePaths(...paths: string[]): string {
    return paths
        .flatMap(path => path.split(/[\\/]/))
        .join('/');
}