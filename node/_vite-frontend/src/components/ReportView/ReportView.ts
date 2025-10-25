import { isNullOrUndefined } from "../../../../kozubenko/utils.js";


export class ReportView {
    static ID = 'report-view';

    static Render(onto:HTMLElement) {
        if(isNullOrUndefined(onto)) {
            console.error('ReportView.Render(): onto[HtmlElement] is null/undefined. Cannot complete Render...');
            return;
        }

        onto.replaceWith(ReportView.generateView());
    }

    static generateView(): HTMLDivElement {
        const view = Object.assign(document.createElement('div'), {
            id: ReportView.ID
        });

        return view;
    }
}