import { Router, Routes } from "../../routes";


export class HomeBtn {
    static ID = 'home-btn';

    /** The onclick method */
    static onclick() {
        if(Router.isAt(Routes.Index) && !window.location.search)
            return;

        window.history.pushState({}, '', Routes.Index);
        window.location.reload();
    }

    
}

const homeBtn = document.getElementById(HomeBtn.ID) as HTMLDivElement;
homeBtn ? homeBtn.onclick = HomeBtn.onclick
        : console.error(`#${HomeBtn.ID} not found during side-effect load! Unable to add onclick[EventListener].`);

homeBtn.addEventListener("keydown", e => {
    if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        homeBtn.click();
    }
});


