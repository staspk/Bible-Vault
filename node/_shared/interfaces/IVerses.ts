/**
    THIS IS NOT CURRENTLY USED ANYWHERE. JUST THEORY, ATM.
*/

import { Book } from "../../models/Bible.js";

export interface IPassage {
    book: Book;
    chapter: number;
    verses: number[];
}

export class IVerses {
    
}