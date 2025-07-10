import { Status } from "./enums.js";


/**
* **Example:**
* ```json
* {
*   "status": "partial",
*   "data": {
*     "KJV": null,
*     "NKJV": {
*       "1": "This is the book of the genealogy of Adam. In the day that God created man, He made him in the likeness of God.",
*       "2": "He created them male and female, and blessed them and called them Mankind in the day they were created.",
*       ...
*     },
*     "RSV": {
*       "1": "This is the book of the generations of Adam. When God created man, he made him in the likeness of God.",
*       ...
*     },
*     "NRSV": {
*       "1": "This is the list of the descendants of Adam. When God created humans, he made them in the likeness of God.",
*       ...
*     },
*     "NASB": {
*       "1": "This is the book of the generations of Adam. On the day when God created man, He made him in the likeness of God.",
*       ...
*     }
*   }
* }
* ```
*/
export interface IChapterResponse {
    status: `${Status}`;
    data: {
        [translation: string]: { [verseNumber: string]: string } | null;
    }
}
/**
* Alternate interfaces for IChapterResponse:
* 
* export interface IChapterResponse {
*     status: `${Status}`;
*     data: {
*         [translation in SupportedBibleTranslations]?: {
*             [verseNumber: string]: string;
*         } | null;
*     };
* }
* 
* export interface IChapterResponse {
*     status: `${Status}`;
*     data: Array<{
*         translation: SupportedBibleTranslations;
*         verses: {
*             [verseNumber: string]: string;
*         } | null;
*     }>;
* }
*/


