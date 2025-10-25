import { Search } from "../../services/Search.js";


export class SearchInput {
    static ID = 'search-input';

    static debounceTimerId;

    static Set(str:string) {
        const searchInput = document.getElementById(SearchInput.ID) as HTMLInputElement;
        if(!searchInput) {  console.error(`SearchInput.Set(): searchInput not found via #${SearchInput.ID}.`); return;  }

        searchInput.value = str;
        searchInput.dispatchEvent(new Event('input', { bubbles: true }));
    }

    static input(event: Event) {
        clearTimeout(SearchInput.debounceTimerId);
    
        const searchStr = (event.target as HTMLInputElement).value.trim();
        if (!searchStr) return;
        
        SearchInput.debounceTimerId = setTimeout(async () => {
            const searchType  = Search.Analyze(searchStr);
        }, 750);
    }
}


const searchInput = document.getElementById(SearchInput.ID);
searchInput ? searchInput.addEventListener('input', SearchInput.input)
            : console.error(`#${SearchInput.ID} not found during side-effect load! Unable to add input[EventListener].`);