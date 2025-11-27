import { TRANSLATIONS } from "../../../index.js";
import { PassageView } from "../PassageView/PassageView.js";
import { ApiEndpoints } from "../../../../_shared/ApiEndpoints.js";
import { BibleApi } from "../../models/BibleApi.js";
import { BibleSearch } from "../../models/BibleSearch.js";
import { Search } from "../../services/Search.js";
import type { IChapterResponse } from "../../../../_shared/interfaces/IResponses.js";
import type { Book } from "../../models/Bible.js";


export class SearchInput {
    static ID = 'search-input';

    static debounceTimerId:any;

    static Set(str:string) {
        const searchInput = document.getElementById(SearchInput.ID) as HTMLInputElement;
        if(!searchInput) {  console.error(`SearchInput.Set(): searchInput not found via #${SearchInput.ID}.`); return;  }

        searchInput.value = str;
        searchInput.dispatchEvent(new Event('input', { bubbles: true }));
    }

    static input(event:Event) {
        clearTimeout(SearchInput.debounceTimerId);

        const searchStr = (event.target as HTMLInputElement).value.trim();
        if (!searchStr) return;
        
        SearchInput.debounceTimerId = setTimeout(async () => {
            const search = new Search(searchStr);

            if(search.data instanceof BibleSearch) {
                const queryString = BibleApi.From(search.data, TRANSLATIONS as string[]).queryString();

                const response = await fetch(`${ApiEndpoints.Bible}${queryString}`);
                if (response.status !== 200) return;

                PassageView.Render(search.data.chapter, (await response.json() as IChapterResponse).data);
                window.history.pushState({}, '', queryString);

                document.title = search.data.toString();
            }
        }, 200);
    }
}


const searchInput = document.getElementById(SearchInput.ID);
searchInput ? searchInput.addEventListener('input', SearchInput.input)
            : console.error(`#${SearchInput.ID} not found during side-effect load! Unable to add input[EventListener].`);