/** A hotstring, at its core. `Document(tagName, options)` =>  

`Object.assign(document.createElement(tagName), {options} ) ` */
export function Document(
    tagName: string,
    options?: object | undefined
) {
    return Object.assign(document.createElement(tagName), options) as HTMLDivElement;
}
export namespace Document {
    /**
    - `window.history.pushState({}, '', route)`
    - `document.title = title`
    */
    export function Title(title:string, route:string) {
        window.history.pushState({}, '', route);
        document.title = title;
    }

    export function CSS_Property(selector_name:string) {
        let sheet = document.styleSheets[0];
        for (const rule of sheet.cssRules)
            if (rule.selectorText === selector_name && rule instanceof CSSStyleRule)
                return rule;
    }
}