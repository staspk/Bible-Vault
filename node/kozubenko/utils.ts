
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

/**
 * Extracts an unsigned int from the end of a given string.
 *
 * @returns {[number, string]} Tuple [number, string]:
 *   - A positive number (or null, if last letter's charCode <48 || >57).
 *   - Remaining string (or '', if entire string was a number)
 * 
 * @example
 * yankIntFromEnd("chapter42") // returns: [42, "chapter"]
 * yankIntFromEnd("file007")   // returns: [7, "file00"]
 * yankIntFromEnd("file")      // returns: [null, "file"]
 */
export function yankUIntFromEnd(string:string): [number, string] | [null, string] {
    let i = string.length - 1;
    for(i; i > -1; i--) {
        const charCode = string.charCodeAt(i);   // 48-57
        if(charCode < 48 || charCode > 57) {
            if(i === string.length - 1)
                return [null, string];
            break;
        }
    }
    const uint:number = parseInt(string.substring(i + 1, string.length), 10)
    return [uint, string.substring(0, (string.length - uint.toString().length))];
}

export function isNullOrUndefined(value):boolean {
    return (value === null || value === undefined) ? true : false;
}

/** Must `await` */
export function sleep(ms:number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}






export function debounce(fn, delay = 100) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };
}