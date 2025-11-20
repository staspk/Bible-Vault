import type { Book } from "../models/Bible.js";
import type { BibleSearch } from "../models/BibleSearch.js";

/** `/api/bible` */
export class BibleApi {
    static translationsDefault = ['KJV,NASB,RSV,RUSV,NKJV,ESV,NRSV,NRT'];

    constructor(
        public book: Book,
        public chapter: number,
        public chapterEnd?: number,
        public verse?: number,
        public verseEnd?: number,
        public translations: string[] = BibleApi.translationsDefault,
    ) { }

    /** *Static Constructor* */
    static From(search:BibleSearch, translations?:string[]) {
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