import { Document } from "../../../kozubenko.ts/Document.js";
import { Api } from "../../api/Api.js";
import { Routes } from "../../services/Router.js";
import { ReportView } from "../ReportView/ReportView.js";


export class ReportBtn {
    static ID = 'report-btn';

    /** The onclick method */
    static onclick() {
        const translations = Array.from(Api.BibleReport.DEFAULT_TRANSLATIONS);
        Document.Title("Data Integrity Report", translations, `${Routes.Report}?translations=${translations}`);
        ReportView.Render(translations);
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