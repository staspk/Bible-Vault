import { ContentView } from "..";
import { ReportView } from "./components/ReportView/ReportView";
import { Document } from "../kozubenko.ts/Document";

export const Routes = {
    Index : '/',
    Report: '/report'
}

export class Router {
    static isAt(route:string) {
        return (window.location.pathname === route)
    } 
}

window.addEventListener('popstate', (e) => {
    const view = e.state?.view;

    if(view === Routes.Index) ContentView.PlaceHolder().replaceWith(Document('div', {id: 'content-view-placeholder'}));
    if(view === Routes.Report) ReportView.Render();
});