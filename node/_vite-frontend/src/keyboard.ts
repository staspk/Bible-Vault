import { PassageView } from "./components/PassageView/PassageView.js";
import { LocalStorage } from "./storage/LocalStorage.js";
import { LocalStorageKeys } from "./storage/LocalStorageKeys.enum.js";


document.addEventListener("keydown", (event) => {
    if(event.key === "ArrowLeft") {
        PassageView.toggleView();
    }

    if(event.key === "ArrowRight") {
        PassageView.toggleView();
    }

    if (event.ctrlKey && event.key === 'm') {
        LocalStorage.toggleBoolean(LocalStorageKeys.mirrorOption);
        window.location.reload();
    }
});