import { ApiEndpoints } from "../../../_shared/ApiEndpoints.js";
import type { BibleTranslation } from "../../../_shared/BibleTranslations.js"
import type { IReportResponse } from "../../../_shared/interfaces/IResponses.js";


/** `/api/bible-report` */
export class BibleReportApi {
    static translationsDefault = ['KJV','NASB','RSV','RUSV','NKJV','ESV','NRSV','NRT'] as BibleTranslation[];

    static async Fetch(translations:BibleTranslation[]=this.translationsDefault): Promise<IReportResponse|false> {
        const response = await fetch(`${ApiEndpoints.Bible_Report}?translations=${translations.toString()}`);
        if(response.status !== 200) {
            console.error(`${BibleReportApi.name}: '${ApiEndpoints.Bible_Report}' => ${response.status}`)
            return false;
        }
        return await response.json() as IReportResponse;
    }
}