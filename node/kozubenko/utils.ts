/**
 * Use to enforce type at runtime. Either returns true, or throws Error
 * 
 * Example Use: `const aString = "hello"; assert_string("aString", aString)`
 */
export function assert_string(varName: string, value: any): true | Error {  
  if (typeof value !== "string") {
    throw new Error(`${varName} must be a string, but is: ${typeof value}`);
  }
  return true
}