import { Routes } from "../../routes";


export class HomeBtn {
    static ID = 'home-btn';

    /** The onclick method */
    static onclick() {
        if(window.location.pathname === Routes.Index && !window.location.search)
            return;

        window.history.pushState({}, '', Routes.Index);
        window.location.reload();
    }
}

const homeBtn = document.getElementById(HomeBtn.ID);
homeBtn ? homeBtn.onclick = HomeBtn.onclick
        : console.error(`#${HomeBtn.ID} not found during side-effect load! Unable to add onclick[EventListener].`);