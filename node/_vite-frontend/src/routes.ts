import { ContentView } from "../index.js";
import { ReportView } from "./components/ReportView/ReportView.js";
import { Document } from "../kozubenko.ts/Document.js";


export const Routes = {
    Index : '/',
    Report: '/report'
} as const;

export class Router {
    static isAt(route:string) {
        return (window.location.pathname === route)
    }
}