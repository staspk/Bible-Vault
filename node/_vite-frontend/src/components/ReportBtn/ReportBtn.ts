import { Routes } from "../../routes.js";
import { ContentView } from "../../../index.js";
import { ReportView } from "../ReportView/ReportView.js";


export class ReportBtn {
    static ID = 'report-btn';

    /** The callback attached on `DOMContentLoaded` */
    static onclick() {
        ReportView.Render(ContentView.PlaceHolder())
        window.history.pushState({}, '', Routes.Report);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const reportBtn = document.getElementById(ReportBtn.ID);
    if(!reportBtn) {  console.error(`#${ReportBtn.ID} not found! Unable to add `); return;  }

    reportBtn.onclick = ReportBtn.onclick;
});