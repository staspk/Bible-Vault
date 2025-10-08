import { Routes } from "../../routes";

export class ReportBtn {
    static ID = 'report-btn';

    /** The callback attached on `DOMContentLoaded` */
    static onclick() {
        window.location.href = Routes.Report
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const reportBtn = document.getElementById(ReportBtn.ID);
    if(!reportBtn) {  console.error(`#${ReportBtn.ID} not found! Unable to add `); return;  }

    reportBtn.onclick = ReportBtn.onclick;
});