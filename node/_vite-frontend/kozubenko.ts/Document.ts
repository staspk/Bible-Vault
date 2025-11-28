

/** A hotstring, at its core. `Document(tagName, options)` becomes:  

`Object.assign(document.createElement(tagName), {options} ) ` */
export function Document(
    tagName: string,
    options?: object | undefined
) {
    return Object.assign(document.createElement(tagName), options)
}