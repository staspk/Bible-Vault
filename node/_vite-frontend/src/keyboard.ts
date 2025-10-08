import { PassageView } from "./components/PassageView/PassageView.js";


document.addEventListener("keydown", (event) => {
    if(event.key === "ArrowLeft") {
        PassageView.toggleView();
    }

    if(event.key === "ArrowRight") {
        PassageView.toggleView();
    }
});