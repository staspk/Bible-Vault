import { isNullOrWhitespace, isPositiveInteger } from "../../../kozubenko/string.extensions.js";
import { yankUIntFromEnd } from "../../../kozubenko/utils.js";
import { Book } from "../models/Bible.js";
import { BookSearch } from "../models/BookSearch.js";
import { Passage } from "../models/Passage.js";


export type searchStr = string;

/** The legal forms/shapes of `Search` */
export enum SearchType {
    /** ie: `"Matthew 10"` */
    IChapter  = "IChapter",
    /** ie: `"Matthew 10:1"` */
    IChapterVerse = "IChapterVerse",
    /** ie: `"Matthew 10:1-2"` */
    IChapterVerses = "IChapterVerses",

    /** ie: `"Matthew 10-11"` */
    // IChapters = "IChapters",

    /** Not one of the other `SearchType.values` */
    Garbage   = "Garbage"
}

export class Search {
    type: SearchType;
    data: Passage;

    constructor(search:string) {
        const potentialBookChapter = search.split(":")[0];
        const potentialVerses      = search.split(":")[1];

        if(isNullOrWhitespace(potentialBookChapter)) {  this.type === SearchType.Garbage;  return;  }

        let book:Book|null, chapter, verseStart, verseEnd;

        const [uint, potentialBook] = yankUIntFromEnd(potentialBookChapter.split("-")[0]);
        if (!uint) {  this.type === SearchType.Garbage;  return;  }

        book    = BookSearch(potentialBook.trim());
        chapter = uint;

        if (!book) {                                  this.type = SearchType.Garbage;  return;  }   // after: legal Book
        if (chapter < 0 || chapter > book.chapters) { this.type = SearchType.Garbage;  return;  }   // after: legal Book.chapter
        
        if(!isNullOrWhitespace(potentialVerses)) {
            verseStart = potentialVerses.split("-")[0]
            verseEnd   = potentialVerses.split("-")[1]

            if(!isPositiveInteger(verseStart)) {  this.type = SearchType.Garbage;  return;  }

            if(!isPositiveInteger(verseEnd)) {
                if(potentialVerses.endsWith("-")) {
                    /*  "Matthew 10:1-"  */
                    this.type = SearchType.IChapterVerses;
                    this.data = new Passage(book, chapter, Number(verseStart.trim()), book.totalVerses(chapter));
                    return;
                }
                /*  "Matthew 10:1"  */
                this.type = SearchType.IChapterVerse;
                this.data = new Passage(book, chapter, Number(verseStart.trim()), undefined);
                return;  
            }
            /*  "Matthew 10:1-2"  */
            this.type = SearchType.IChapterVerses
            this.data = new Passage(book, chapter, Number(verseStart.trim()), Number(verseEnd.trim()));
            return;        
        }
        /*  "Matthew 10"  */
        this.type = SearchType.IChapter;
        this.data = new Passage(book, chapter, undefined, undefined);
        return;     
    }
}