import { DEFINITIONS_TS } from "./definitions.js";
import { assert_string } from "./kozubenko/utils";
import { print } from "./kozubenko/print.js";

console.log("DEFINITIONS_TS:", DEFINITIONS_TS);
print("DEFINITIONS_TS", DEFINITIONS_TS);

const aString = "hello";
assert_string("aString", aString)