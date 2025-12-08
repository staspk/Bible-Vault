import { ContentView } from "../../../index.js";
import { Router, Routes } from "../../services/Router.js";
import { SearchInput } from "../SearchInput/SearchInput.js";


/** Requires: side-effect load. */
export class HomeBtn {
    static ID = 'home-btn';

    /** The onclick method */
    static onclick() {
        if(Router.isHome())
            return;

        window.history.pushState({}, '', Routes.Index);
        ContentView.Reset()
        SearchInput.Set("");
        SearchInput.Placeholder('John 1:8-12');
    }
}

const homeBtn = document.getElementById(HomeBtn.ID) as HTMLDivElement;
homeBtn ? homeBtn.onclick = HomeBtn.onclick
        : console.error(`#${HomeBtn.ID} not found during side-effect load! Unable to add onclick[EventListener].`);

homeBtn.addEventListener("keydown", e => {
    if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        HomeBtn.onclick();
    }
});


