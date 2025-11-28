
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