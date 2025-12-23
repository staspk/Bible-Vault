import { Document } from "../../../kozubenko.ts/Document.js";
import { Search } from "../../services/Search.js";
import { PassageView } from "../PassageView/PassageView.js";
import { ReportView } from "../ReportView/ReportView.js";
import { BookSearch } from "../../models/BookSearch.js";
import { isNullOrWhitespace } from "../../../../kozubenko/string.extensions.js";
import { Router, Routes } from "../../services/Router.js";
import { ContentView } from "../../../index.js";
import { Api } from "../../api/Api.js";
import { Passage } from "../../models/Passage.js";


/** Requires: side-effect load. */
export class SearchInput {
    static ID = 'search-input';
    static Element: HTMLInputElement;

    static Reset() { this.Element.value = ""; }
    static Set(text:string, dispatchInputEvent=true) {
        this.Element.value = text;
        if(dispatchInputEvent) this.Element.dispatchEvent(new Event('input', { bubbles: true }));
    }

    static debounceTimer:any;
    static input(event:Event) {
        clearTimeout(SearchInput.debounceTimer);

        const searchStr = (event.target as HTMLInputElement).value.trim();
        if (!searchStr && Router.isAt(Routes.Index)) return;
        
        SearchInput.debounceTimer = setTimeout(async () => {
            if(Router.isAt(Routes.Index)) {
                const search = new Search(searchStr);
                if(search.data instanceof Passage) {
                    const passage = search.data;
                    Document.Title(passage.toString(), passage, Api.Passage.From(passage).queryString());
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