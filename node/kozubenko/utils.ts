
export class Paths {
    /**
     * Handles paths with any combination of forward `/` and backslashes `\`.
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

/**
 * Note: also handles `undefined` (returns: `True`)
 */
export function isNullOrWhitespace(str:string): boolean {
    if(str == null || str.trim() === "")
        return true;
    return false;
}

/**
 *  Essentially, a QoL extension of String.split() to allow direct access and easy manipulation, whether or not separator actually exists. Returned arrays always have a min length of 2.
 * 
 * @example
 * safeSplit("Matthew 10", ":")      // returns ["Matthew 10", null]
 * safeSplit("Matthew 10:12", ":")   // returns ["Matthew 10", "12"]
 */
export function safeSplit(str:string, separator:string|RegExp, limit?:number): string[] {
    const array = str.split(separator, limit);
    if(array == null)
        return [str, null];
    return array;
}


export function isUInt(value): boolean {
    value = parseInt(value);
    if (Number.isInteger(value) && value > 0)
        return true;
    return false;
}