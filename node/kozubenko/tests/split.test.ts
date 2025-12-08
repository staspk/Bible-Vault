/**
    left  = input1.split("-")[0];
    right = input1.split("-")[1];

    right === undefined, when: separator does not exist in input
    right === ''       , when: separator exists, but nothing follows after

    RESULT: safeSplit() is completely unnecessary
*/
import { Print } from "../print.js"
import { safeSplit } from "../string.extensions.js"

const a1 = safeSplit("13", "-")
const a2 = safeSplit("13-14", "-")
const a3 = safeSplit("13-", "-")

const b1 = "13".split("-")
const b2 = "13-14".split("-")
const b3 = "13-".split("-")


const input1 = "13"
const input2 = "13-14"
const input3 = "13-"

const input1_left  = input1.split("-")[0];
const input1_right = input1.split("-")[1];

const input2_left  = input2.split("-")[0];
const input2_right = input2.split("-")[1];

const input3_left  = input3.split("-")[0];
const input3_right = input3.split("-")[1];

Print.yellow(input1)
console.log(b1)
console.log(`${input1_left},${input1_right}`)

console.log('\n')

Print.yellow(input2)
console.log(b2)
console.log(`${input2_left},${input2_right}`)

console.log('\n')

Print.yellow(input3)
console.log(b3)
console.log(`${input3_left},${input3_right}`)