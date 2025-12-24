
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

export function isWhitespace(str:string): boolean {
    return str.trim().length === 0;
}

export function removeWhitespace(str:string): string {
    return str.replace(/\s+/g, '');
}

export function longest_string_length(array:string[]): number {
    let longest_length = 0;
    for (const word of array)
        if(longest_length < word.length) longest_length = word.length;
    return longest_length;
}