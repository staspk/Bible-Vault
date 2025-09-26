import { PassageView } from "./components/PassageView";


document.addEventListener("keydown", (event) => {
    if(event.key === "ArrowLeft") {
        PassageView.toggleView();
    }

    if(event.key === "ArrowRight") {
        PassageView.toggleView();
    }
});