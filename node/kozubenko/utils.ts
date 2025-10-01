
export class Paths {
    /**
     * A QoL Extension of `path.join`. Handles paths with any combination of forward `/` and backslashes `\`.
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