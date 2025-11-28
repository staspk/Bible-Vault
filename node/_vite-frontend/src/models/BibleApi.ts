import type { BibleTranslation } from "../../../_shared/BibleTranslations.js";
import { TRANSLATIONS } from "../../index.js";
import type { Book } from "./Bible.js";
import type { BibleSearch } from "./BibleSearch.js";

/** `/api/bible` */
export class BibleApi {
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

    queryString(): string {
        let QueryString = "?";

        QueryString += `translations=${this.translations.join(',')}`;
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