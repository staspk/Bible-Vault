/**
 *  A QoL extension of `String.split()` to allow direct access and easy manipulation, whether or not separator actually exists. Returned arrays always have a min length of 2.  
 *  Note: behavior mimics PowerShell's `string.split`.
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

/**
 * Note: also handles `undefined` (returns: `True`)
 */
export function isNullOrWhitespace(str:string): boolean {
    if(str == null || str.trim() === "")
        return true;
    return false;
}

export function isUInt(value:string): boolean {
    const _value = parseInt(value);
    if (Number.isInteger(_value) && _value > 0)
        return true;
    return false;
}