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

/**  Note: `undefined` also returns: `True` */
export function isNullOrWhitespace(str:string): boolean {
    if(str == null || str.trim() === "")
        return true;
    return false;
}

export function isPositiveInteger(str:string): boolean {
    const potentialInteger = parseInt(str);
    if (Number.isInteger(potentialInteger) && potentialInteger > 0)
        return true;
    return false;
}