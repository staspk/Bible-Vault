import { isNullOrUndefined } from "../../kozubenko/utils.js";
import type { IViewComponent } from "./IComponentView.js"


/** A hotstring, at its core. `Document(tagName, options)` becomes:  

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

export class Placeholder {
    /** `IViewComponent` `Render()` Helper (First Step).  
      Sets `component.Element` to new DIV(id determined by `component.ID`) that replaces `onto` in the DOM. */
    static ReplaceWith(onto:HTMLElement, component:IViewComponent) {
        if(isNullOrUndefined(onto)) {
            console.error(`${component.name}.Render(): onto is null/undefined. Cannot complete Render...`);
            return false;
        }
        const componentDiv = Document('div', {
            id: component.ID
        }); onto.replaceWith(componentDiv);

        component.Element = componentDiv;
        return component;
    }
}