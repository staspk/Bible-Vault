import { PassageView } from "./components/PassageView/PassageView";
import { LocalStorage } from "./storage/LocalStorage";
import { LocalStorageKeys } from "./storage/LocalStorageKeys.enum";


document.addEventListener("keydown", (event) => {
    if(event.key === "a" || event.key === "d") {
        PassageView.toggleView();
    }

    
    

    if (event.ctrlKey && event.key === 'm') {
        LocalStorage.toggleBoolean(LocalStorageKeys.MIRROR_OPTION);
        window.location.reload();
    }
});