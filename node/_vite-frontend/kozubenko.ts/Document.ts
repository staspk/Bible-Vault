


/** A hotstring, at its core. `Document(tagName, options)` =>  

`Object.assign(document.createElement(tagName), {options} ) ` */
export function Document(
    tagName: string,
    options?: object | undefined
) {
    return Object.assign(document.createElement(tagName), options) as HTMLDivElement;
}
export namespace Document {
    /** `document.title = title` */
    export function Title(title:string) {
        document.title = title;
    }
}