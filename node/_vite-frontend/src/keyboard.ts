import { PassageView } from "./components/PassageView/PassageView";
import { Router, Routes } from "./services/Router";
import { LocalStorage } from "./storage/LocalStorage";
import { LocalStorageKeys } from "./storage/LocalStorageKeys.enum";


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
            
        }
        if(event.ctrlKey && event.key === "ArrowRight") {
            
        }
    }
});