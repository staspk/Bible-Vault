import { Book } from "../../../_shared/Bible";


/** Form Examples:
    - `"John 1"`
    - `"John 1:1"`
    - `"John 1:1-2"` */
export class Passage {
    constructor(
        public book: Book,
        public chapter: number,
        public verse?: number,
        public verseEnd?: number
    ){}

    toString() {
        let str = `${this.book.name} ${this.chapter}`;
        if(this.verse)    str += `:${this.verse}`;
        if(this.verseEnd) str += `-${this.verseEnd}`;
        return str;
    }
}