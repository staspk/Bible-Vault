import { UrlParam, URLQueryParams } from "./URLQueryParams";
import { SearchInput } from "../components/SearchInput/SearchInput";
import type { searchStr } from "./Search";
import { ReportView } from "../components/ReportView/ReportView";
import { ContentView } from "../..";
import { PassageView } from "../components/PassageView/PassageView";
import { ReportBtn } from "../components/ReportBtn/ReportBtn";
import type { Translation } from "../../../_shared/BibleTranslations";
import type { Passage } from "../models/Passage";


export const Routes = {
    Index : '/',
    Report: '/report',
} as const;

export class Router {
    static isHome() {
        if(Router.isAt(Routes.Index) && !window.location.search) return true;
        return false;
    }
    static isAt(route:string) {
        return (window.location.pathname === route)
    }

    constructor() {
        if(Router.isAt(Routes.Report)) {
            const translations = URLQueryParams.translations();
            if(!translations) ReportBtn.onclick();
            else {
                window.history.replaceState(translations, '', `${Routes.Report}?translations=${translations}`);
                document.title = "Data Integrity Report";
                ReportView.Render(translations);
            }
        }
        if(Router.isAt(Routes.Index)) {
            const BOOK    = UrlParam('book');
            const CHAPTER = UrlParam('chapter');
            const VERSES  = UrlParam('verses');

            if(BOOK && CHAPTER) {
                let searchStr = `${BOOK} ${CHAPTER}` as searchStr;
                if(VERSES) {
                    const verseStart = VERSES.split("-")[0];
                    const verseEnd   = VERSES.split("-")[1];
                    
                    searchStr += `:${verseStart}`;
                    if(verseEnd) searchStr += `-${verseEnd}`;
                }
                SearchInput.Set(searchStr);
            }
        }
    }
}

window.addEventListener("popstate", (state) => {
    if(Router.isHome())                 ContentView.Reset();
    else if(Router.isAt(Routes.Index))  PassageView.Render(state.state as Passage);
    else if(Router.isAt(Routes.Report)) ReportView.Render(state.state as Translation[])
});