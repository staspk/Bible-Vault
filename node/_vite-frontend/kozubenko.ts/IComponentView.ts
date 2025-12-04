import { isNullOrUndefined } from "../../kozubenko/utils.js";
import { Document } from "./Document.js";


/** static interface */
export interface IViewComponent {
    ID:string;
    Element:any;

    /** (built-in) class name */
    name:string;
}

export class IViewComponent {

    /** First Step of an IViewComponent `Render()`:
    - `isNullOrUndefined(onto)` Assertion - `console.error` report, If: `true`
    - `component.ID` determines `id` of new Div that replaces `onto` in the DOM.
    - `component.Element` becomes ptr to the new Div
     */
    static ReplaceWith(onto:HTMLElement, component:IViewComponent): false | IViewComponent {
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