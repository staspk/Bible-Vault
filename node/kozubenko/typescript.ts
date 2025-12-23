

/** Hides ts-compiler inability to detect an optional param gaining value in constructor.  
    Hides ts-compiler error: `Object is possibly 'undefined'`. */
export function enforced_as_number_in_constructor(number:any): number {
    return Number(number);
}