
export class Path {
    /**
     * A QoL Extension of module's `path.join()`. Handles paths with any combination of forward `/` and backslashes `\`.
     *
     * @returns {string} Returns a path with forward slashes `/`
     */
    static safeJoin(...paths: string[]): string {
        return paths
            .flatMap(path => path.split(/[\\/]/))
            .filter(path => path)
            .join('/');
    }
}

export function isNullOrUndefined(value):boolean {
    return (value === null || value === undefined) ? true : false;
}