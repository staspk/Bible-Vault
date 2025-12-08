import { ContentView, TRANSLATIONS } from "../../../index.js";
import { PassageView } from "../PassageView/PassageView.js";
import { ApiEndpoints } from "../../../../_shared/ApiEndpoints.js";
import { BibleApi } from "../../models/BibleApi.js";
import { BibleSearch, BookSearch } from "../../models/BibleSearch.js";
import { Search } from "../../services/Search.js";
import type { IChapterResponse } from "../../../../_shared/interfaces/IResponses.js";
import { Router, Routes } from "../../routes.js";
import { ReportView } from "../ReportView/ReportView.js";
import { isNullOrWhitespace } from "../../../../kozubenko/string.extensions.js";


/** Requires: side-effect load. */
export class SearchInput {
    static ID = 'search-input';
    static Element: HTMLInputElement;

    static Set(text:string) {
        this.Element.value = text;
        this.Element.dispatchEvent(new Event('input', { bubbles: true }));
    }

    static debounceTimer:any;
    static input(event:Event) {
        clearTimeout(SearchInput.debounceTimer);

        const searchStr = (event.target as HTMLInputElement).value.trim();
        if (!searchStr && Router.isAt(Routes.Index)) return;
        
        SearchInput.debounceTimer = setTimeout(async () => {
            if(Router.isAt(Routes.Index)) {
                const search = new Search(searchStr);
                if(search.data instanceof BibleSearch) {
                    PassageView.Render(search.data, ContentView.PlaceHolder());
                }
                return;
            }
            if(Router.isAt(Routes.Report)) {
                const book = BookSearch(searchStr);
                if(book) ReportView.Highlight(book);

                if(isNullOrWhitespace(searchStr))
                    ReportView.Unhighlight();
            }
        }, 200);
    }

    static Placeholder(text:string) {
        this.Element.placeholder = text;
    } 
}


SearchInput.Element = document.getElementById(SearchInput.ID) as HTMLInputElement;
SearchInput.Element ? SearchInput.Element.addEventListener('input', SearchInput.input)
                    : console.error(`#${SearchInput.ID} not found during side-effect load! Unable to add input[EventListener].`);