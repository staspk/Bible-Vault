import { PassageDiv } from "./components/PassageDiv";


document.addEventListener("keydown", (event) => {
    if(event.key === "ArrowLeft") {
        PassageDiv.toggleView();
    }

    if(event.key === "ArrowRight") {
        PassageDiv.toggleView();
    }
});