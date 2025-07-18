/**
* pretty-prints pairs of `varName:string`, `value:any` to console. Prints to one line. Keep `str[].length < ~10`
* 
* Required: `vars.length === 1 || vars.length === % 2 == 0`
*
* Example Usage: `print('name', name, 'age', 30, 'aList', aList)`
*/
export function print(...vars) {
    if (vars.length === 1) {
        console.log(vars[0]);
        return;
    }
    
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


/**
 * Extracts an unsigned int from the end of a given string.
 *
 * @returns {[number, string]} Tuple [number, string]:
 *   - A positive number (or null, if last letter's charCode <48 || >57).
 *   - Remaining string (or '', if entire string was a number)
 * 
 * @example
 * yankIntFromEnd("chapter42") // returns [42, "chapter"]
 * yankIntFromEnd("file007")   // returns [7, "file00"]
 */
export function yankUIntFromEnd(string:string): [number, string] {
    let i = string.length - 1;
    for(i; i > -1; i--) {
        const charCode = string.charCodeAt(i);   // 48-57
        if(charCode < 48 || charCode > 57) {
            if(i === string.length - 1)
                return [null, string];
            break;
        }
    }
    const int:number = parseInt(string.substring(i + 1, string.length), 10)
    return [int, string.substring(0, (string.length - int.toString().length))];
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