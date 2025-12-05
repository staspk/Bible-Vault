import { ApiEndpoints } from "../../../_shared/ApiEndpoints.js";
import type { BibleTranslation } from "../../../_shared/BibleTranslations.js";
import type { IChapter, IChapterResponse } from "../../../_shared/interfaces/IResponses.js";
import { TRANSLATIONS } from "../../index.js";
import type { Book } from "./Bible.js";
import type { BibleSearch } from "./BibleSearch.js";


/** `/api/bible` */
export class BibleApi {
    static ENDPOINT = ApiEndpoints.Bible;

    static translationsDefault = ['KJV','NASB','RSV','RUSV','NKJV','ESV','NRSV','NRT'] as BibleTranslation[];

    constructor(
        public book: Book,
        public chapter: number,
        public chapterEnd?: number,
        public verse?: number,
        public verseEnd?: number,
        public translations: string[] = TRANSLATIONS
    ){}

    /** *Static Constructor* */
    static From(search:BibleSearch, translations:string[]=TRANSLATIONS) {
        return new BibleApi(search.book, search.chapter, search.chapterEnd, search.verse, search.verseEnd, translations);
    }

    static async Fetch(query:string): Promise<IChapter|false> {
        const response = await fetch(`${this.ENDPOINT}${query}`);
        if(response.status !== 200) {
            console.error(`${this.name}: '${this.ENDPOINT}' => ${response.status}`);
            return false;
        }
        return (await response.json() as IChapterResponse).data;

    }

    queryString(): string {
        let QueryString = "?";

        QueryString += `translations=${this.translations.toString()}`;
        QueryString += `&book=${this.book.name}`;
        QueryString += `&chapter=${this.chapter}`;

        if(this.chapterEnd) {
            QueryString += `-${this.chapterEnd}`;
            return QueryString;
        }

        if(this.verse) {
            QueryString += `&verses=${this.verse}`;

            if(this.verseEnd)
                QueryString += `-${this.verseEnd}`;
        }

        return QueryString;
    }
}