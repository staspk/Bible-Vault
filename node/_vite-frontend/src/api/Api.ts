import { PassageApi } from "./Passage.js"
import { BibleReportApi } from "./BibleReport.js"


export const Api = {
    Passage: PassageApi,
    BibleReport: BibleReportApi
} as const;
