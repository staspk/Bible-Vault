function type(value) {
    if (value === null) return "null";
    if (value === undefined) return "undefined";
    
    const type = typeof value;
    if (type !== "object")  return type; // "string", "number", "boolean", "function", "symbol", "bigint"
    
    if (Array.isArray(value)) return "array";
    if (value instanceof Error) return "error";
    if (value instanceof Promise) return "promise";
    if (value instanceof Map) return "map";
    if (value instanceof Set) return "set";

    if (value instanceof Date) return "date";
    if (value instanceof RegExp) return "regexp";
    if (value instanceof WeakMap) return "weakmap";
    if (value instanceof WeakSet) return "weakset";   
}

/**
* Use to enforce type at runtime. Either returns true, or throws Error
* 
* Example Use: `const aString = "hello"; assert_string("aString", aString)`
*/
export function assert_string(varName: string, value: any): true | Error {  
    if (typeof value !== "string") {
        throw new Error(`${varName} must be a string, but is: ${typeof value}`);
    }
    return true;
}

/**
* Use to enforce type at runtime. Either returns true, or throws Error (if not 'number' or 'bigint')
* 
* Example Use: `const aNumber = 5; assert_int("aNumber", aNumber)`
*/
export function assert_number(varName: string, value: any, minVal?: number, maxVal?: number): true | Error {  
    if (typeof value !== "number" && typeof value !== "bigint")
        throw new Error(`assert_number(${varName}): must be a number, but is: ${typeof value}`);

    if (minVal !== undefined && value < minVal)
        throw new Error(`assert_number(${varName}): value less than min_val. min_val: ${minVal}. value: ${value}`);

    if (maxVal !== undefined && value > maxVal)
        throw new Error(`assert_number(${varName}): value greater than min_val. max_val: ${maxVal}. value: ${value}`);

    return true;
}

/**
* Use to enforce type at runtime. List refers to string[]. Either returns true, or throws Error
* 
* Example Use: `const aList = ["hello", "goodbye"]; assert_list("aList", aList)`
*/
export function assert_list(varName: string, value: any): true | Error {  
    if (Array.isArray(value)) {
        throw new Error(`${varName} must be a string[], but is: ${typeof value}`);
    }
    return true;
}

/**
* Use to enforce type at runtime. Either returns true, or throws Error
* 
* Example Use: `const aString = "hello"; assert_string("aString", aString)`
*/
export function assert_class(varName: string, value: any, classType: any): true | Error {  
    if (!(value instanceof classType)) {
        throw new Error(`${varName} must be a ${classType.name}, but is: ${value.name}}`);
    }
    return true;
}