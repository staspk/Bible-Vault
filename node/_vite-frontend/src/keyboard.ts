import { Document } from "../kozubenko.ts/Document";
import { Api } from "./api/Api";
import { BIBLE, ChapterPtr } from "../../_shared/Bible";
import { PassageView } from "./components/PassageView/PassageView";
import { Passage } from "./models/Passage";
import { Router, Routes } from "./services/Router";
import { LocalStorage } from "./storage/LocalStorage";
import { LocalStorageKeys } from "./storage/LocalStorageKeys.enum";
import { SearchInput } from "./components/SearchInput/SearchInput";


document.addEventListener("keydown", (event) => {

    if(Router.isAt(Routes.Index) && !Router.isHome())
    {
        if(event.ctrlKey && event.key === 'm') {
            LocalStorage.toggleBoolean(LocalStorageKeys.MIRROR_OPTION);
            window.location.reload();
        }

        if(event.key === "ArrowLeft")  PassageView.toggleView();
        if(event.key === "ArrowRight") PassageView.toggleView();

        if(event.ctrlKey && event.key === "ArrowLeft") {
            const ptr = new ChapterPtr(PassageView.passage.book, PassageView.passage.chapter).decrement();
            const passage = new Passage(ptr.book, ptr.chapter);

            Document.Title(passage.toString(), passage, Api.Passage.From(passage).queryString());
            SearchInput.Set(passage.toString(), false);
            PassageView.Render(passage);
            window.scrollTo({ top: 0, behavior: "instant" });
            return;
        }
        if(event.ctrlKey && event.key === "ArrowRight") {
            const ptr = new ChapterPtr(PassageView.passage.book, PassageView.passage.chapter).increment();
            const passage = new Passage(ptr.book, ptr.chapter);

            Document.Title(passage.toString(), passage, Api.Passage.From(passage).queryString());
            SearchInput.Set(passage.toString(), false);
            PassageView.Render(passage);
            window.scrollTo({ top: 0, behavior: "instant" });
            return;
        }
    }

    if(Router.isHome()) {
        if(event.ctrlKey && event.key === "ArrowLeft") {
            const passage = new Passage(BIBLE.REVELATION, 22);

            Document.Title(passage.toString(), passage, Api.Passage.From(passage).queryString());
            SearchInput.Set(passage.toString(), false);
            PassageView.Render(passage);
            return;
        }
        if(event.ctrlKey && event.key === "ArrowRight") {
            const passage = new Passage(BIBLE.GENESIS, 1);

            Document.Title(passage.toString(), passage, Api.Passage.From(passage).queryString());
            SearchInput.Set(passage.toString(), false);
            PassageView.Render(passage);
            return;
        }
    }
});