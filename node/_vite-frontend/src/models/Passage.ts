import { Book } from "./Bible";


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