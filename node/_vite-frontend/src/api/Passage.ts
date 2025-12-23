import { ApiEndpoints } from "../../../_shared/ApiEndpoints.js";
import type { BibleTranslation } from "../../../_shared/BibleTranslations.js";
import type { IChapterResponse } from "../../../_shared/interfaces/IResponses.js";
import type { Book } from "../../../_shared/Bible.js";
import { Passage } from "../models/Passage.js";
import { URLQueryParams } from "../services/URLQueryParams.js";
import { LocalStorage } from "../storage/LocalStorage.js";
import { LocalStorageKeys } from "../storage/LocalStorageKeys.enum.js";


/** `/api/passage` */
export class PassageApi {
    static ENDPOINT = ApiEndpoints.Passage;

    static translationsDefault = ['KJV','NASB','RSV','RUSV','NKJV','ESV','NRSV','NRT'] as BibleTranslation[];

    constructor(
        public translations: BibleTranslation[],
        public book: Book,
        public chapter: number,
        public verse?: number,
        public verseEnd?: number
    ){}

    /** *Static Constructor* */
    static From(
        passage:Passage,
        translations = URLQueryParams.translations() ?? LocalStorage.getArray(LocalStorageKeys.TRANSLATIONS) as BibleTranslation[]
    ) {
        return new PassageApi(translations, passage.book, passage.chapter, passage.verse, passage.verseEnd);
    }

    static async Fetch(query:string): Promise<IChapterResponse|false> {
        const response = await fetch(`${this.ENDPOINT}${query}`);
        if(response.status !== 200) {
            console.error(`${this.name}: '${this.ENDPOINT}' => ${response.status}`);
            return false;
        }
        return (await response.json() as IChapterResponse);
    }

    queryString(): string {
        let queryString = "?";

        queryString += `translations=${this.translations.toString()}`;
        queryString += `&book=${this.book.name}`;
        queryString += `&chapter=${this.chapter}`;

        if(this.verse) {
            queryString += `&verses=${this.verse}`;
            if(this.verseEnd)
                queryString += `-${this.verseEnd}`;
        }

        return queryString;
    }
}

