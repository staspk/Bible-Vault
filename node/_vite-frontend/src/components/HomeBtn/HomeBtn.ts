import { ContentView } from "../../../index.js";
import { Router, Routes } from "../../routes.js";
import { Document } from "../../../kozubenko.ts/Document.js"
import { SearchInput } from "../SearchInput/SearchInput.js";


/** Requires: side-effect load. */
export class HomeBtn {
    static ID = 'home-btn';

    /** The onclick method */
    static onclick() {
        if(Router.isAt(Routes.Index) && !window.location.search)
            return;

        window.history.pushState({}, '', Routes.Index);
        ContentView.PlaceHolder().replaceWith(Document('div', {id: 'content-view-placeholder'}))
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


