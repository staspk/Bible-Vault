/**
* pretty-prints pairs of `varName:string`, `value:any` to console. Prints to one line. Keep `str[].length < ~10`
* 
* Required: `vars.length % 2 === 0`
*
* Example Usage: `print('name', name, 'age', 30, 'aList', aList)`
*/
export function print(...vars) {
    if (vars.length % 2 !== 0) {
        console.error(`print expects an even number of arguments. got: ${vars.length}`);    return;
    }
    
    let formatString = '';
    for (let i = 0; i < vars.length; i += 2) {
        const varName = vars[i];
        let   value   = vars[i + 1];
        if (Array.isArray(value)) {
            value = ((value) => 
                '[' + (value.map(el => typeof el === 'string' ? `'${el}'` : el).join(', ')) + ']'
            )(value);
        }
        formatString += `%c${varName}:%c ${value} `;
    }
    console.log(formatString.trim(), ...new Array(vars.length / 2).fill(['color: gold', 'color: yellow']).flat());
}

export function printGreen(text) {
    console.log('%c' + text, 'color: green');
}

export function printYellow(text) {
    console.log('%c' + text, 'color: yellow');
}

export function printRed(text) {
    console.log('%c' + text, 'color: red');
}


/**
 * Extracts an integer from the end of the given string.
 *
 * @param {string} string - The input string to process.
 * @returns {[number, string]} A tuple where the first element is the integer
 *                              yanked from the end of the string, and the second
 *                              is the remaining string with the integer removed.
 *
 * @example
 * yankIntFromEnd("chapter42") // returns [42, "chapter"]
 * yankIntFromEnd("file007")   // returns [7, "file"]
 */
export function yankIntFromEnd(string) {
    
}

/**
 *  Necessary in browser js to get vscode intellisense
 */
export function assertInt(str) {
    const result = parseInt(str, 10);
    if (isNaN(result))
        return null;
    return result;
}

/**
 *  Necessary in browser js to get vscode intellisense
 */
export function assertStr(str) {
    const result = String(str);
    if (str !== undefined && str !== null && str !== '')
        return result;
    return null;
}


// EXPERIMENTAL debounce function

// function debounce(fn, delay) {
//     let timeoutId;
//     return (...args) => {
    //         clearTimeout(timeoutId);
//         timeoutId = setTimeout(() => fn(...args). delay);
//     }
// }
// searchInput.addEventListener('input', debounce(async (event) => {
    //     const value = event.target.value.trim();
//     if (!value) return;

//     try {
//         const response = await fetch(`/api/?book=${book}&chapter=${chapter}&translations=${translations}`);
//         if (!response.ok) throw new Error('Network Error');

//         const data = await response.json();
//         console.log('Search results:', data);

//     } catch (error) {
//         console.error()
//     }
// }, 1500));


/// some messed up code