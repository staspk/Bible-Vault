import { Routes } from "../../routes.js";
import { ContentView } from "../../../index.js";
import { ReportView } from "../ReportView/ReportView.js";


export class ReportBtn {
    static ID = 'report-btn';

    /** The onclick method */
    static onclick() {
        ReportView.Render(ContentView.PlaceHolder())
        window.history.pushState({}, '', Routes.Report);
    }
}


const reportBtn = document.getElementById(ReportBtn.ID) as HTMLDivElement;
reportBtn ? reportBtn.onclick = ReportBtn.onclick
          : console.error(`#${ReportBtn.ID} not found during side-effect load! Unable to add onclick[EventListener].`);

reportBtn.addEventListener("keydown", e => {
    if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        ReportBtn.onclick();
    }
});