import { isNullOrWhitespace, isPositiveInteger, safeSplit } from "../../../kozubenko/string.extensions.js";
import { yankUIntFromEnd } from "../../../kozubenko/utils.js";
import { Book } from "../models/Bible.js";
import { BibleSearch } from "../models/BibleSearch.js";


/** The legal forms/shapes of `Search` */
export enum SearchType {
    /** ie: `"Matthew 10"` */
    IChapter  = "IChapter",
    /** ie: `"Matthew 10-11"` */
    IChapters = "IChapters",
    /** ie: `"Matthew 10:1"` */
    IChapterVerse = "IChapterVerse",
    /** ie: `"Matthew 10:1-2"` */
    IChapterVerses = "IChapterVerses",

    /** Not one of the other `SearchType.values` */
    Garbage   = "Garbage"
}

export class Search {
    type: SearchType;
    data: BibleSearch;

    constructor(search:string) {
        const potentialBookChapter = safeSplit(search, ":")[0];
        const potentialVerses      = safeSplit(search, ":")[1];

        if(isNullOrWhitespace(potentialBookChapter)) {  this.type === SearchType.Garbage;  return;  }

        let book:Book|null, chapterStart, chapterEnd, verseStart, verseEnd;

        const [uint, potentialBook] = yankUIntFromEnd(safeSplit(potentialBookChapter, "-")[0]);
        if (!uint) {  this.type === SearchType.Garbage;  return;  }

        book         = BibleSearch.match_bible_book_search_term(potentialBook.trim());
        chapterStart = uint;
        chapterEnd   = safeSplit(potentialBookChapter, "-")[1];
        
        if (!book) {                                            this.type = SearchType.Garbage;  return;  }       // after: legal book (is Book)
        if (chapterStart < 0 || chapterStart > book.chapters) { this.type = SearchType.Garbage;  return;  }       // after: legal chapterStart

        if(isPositiveInteger(chapterEnd)) {
            this.type = SearchType.IChapters;
            this.data = new BibleSearch(book, chapterStart, chapterEnd, undefined, undefined);
            return;     //: "Matthew 10-11"
        }
        
        if(!isNullOrWhitespace(potentialVerses)) {
            verseStart = potentialVerses.split("-")[0]
            verseEnd   = potentialVerses.split("-")[1]

            if(!isPositiveInteger(verseStart)) {  this.type = SearchType.Garbage;  return;  }      // after: verseStart in legal form 

            if(!isPositiveInteger(verseEnd)) {
                if(potentialVerses.endsWith("-")) {
                    /*  "Matthew 10:1-"  */
                    this.type = SearchType.IChapterVerse;
                    this.data = new BibleSearch(book, chapterStart, undefined, verseStart, book.totalVerses(chapterStart));
                    return;
                }
                /*  "Matthew 10:1"  */
                this.type = SearchType.IChapterVerse;
                this.data = new BibleSearch(book, chapterStart, undefined, verseStart, undefined);
                return;  
            }
            /*  "Matthew 10:1-2"  */
            this.type = SearchType.IChapterVerses
            this.data = new BibleSearch(book, chapterStart, undefined, verseStart, verseEnd);
            return;        
        }
        /*  "Matthew 10"  */
        this.type = SearchType.IChapter;
        this.data = new BibleSearch(book, chapterStart, undefined, undefined, undefined);
        return;     
    }
    

    /**  The search string analysis algorithm in simplified form. Note: this is not an exact copy of the constructor form */
    static Analyze(search:string): SearchType {
        const potentialBookChapter = safeSplit(search, ":")[0];
        const potentialVerses      = safeSplit(search, ":")[1];

        if(isNullOrWhitespace(potentialBookChapter))          return SearchType.Garbage;

        let book, chapterStart, chapterEnd, verseStart, verseEnd;

        const [uint, potentialBook] = yankUIntFromEnd(safeSplit(potentialBookChapter, "-")[0]);
        if (!uint)                                            return SearchType.Garbage;

        book         = BibleSearch.match_bible_book_search_term(potentialBook.trim());
        chapterStart = uint;
        chapterEnd   = safeSplit(potentialBookChapter, "-")[1];

        if (!book)                                            return SearchType.Garbage;
        if (chapterStart < 0 || chapterStart > book.chapters) return SearchType.Garbage;

        if(isPositiveInteger(chapterEnd))                     return SearchType.IChapters;          //: "Matthew 10-11"
            
        if(!isNullOrWhitespace(potentialVerses)) {
            verseStart = safeSplit(potentialVerses, "-")[0];
            verseEnd   = safeSplit(potentialVerses, "-")[1];
            
            if(!isPositiveInteger(verseStart))                return SearchType.Garbage;
            if(!isPositiveInteger(verseEnd))                  return SearchType.IChapterVerse;      //: "Matthew 10:1"
            else                                              return SearchType.IChapterVerses;     //: "Matthew 10:1-2"
        }
                                                              return SearchType.IChapter;           //: "Matthew 10"
    }
}