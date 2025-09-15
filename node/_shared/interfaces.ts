import { Status } from "./enums.js";
import { printGreen, printOrange, printYellow } from "./print.js";


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
* **Example:**
* ```json
* {
*   "status": "partial",
*   "data": {
*      "27": {
*         "KJV": null,
*         "NKJV": {
*            "1": Now it came to pass, when Isaac was old and his eyes were so dim that he could not see, that he called Esau his older son and said to him, "My son." And he answered him, "Here I am.",
*            "2": "Then he said, “Behold now, I am old. I do not know the day of my death.",
*            ...
*      },
*      "28": {
*         "KJV": {
*            "1": "And Isaac called Jacob, and blessed him, and charged him, and said unto him, Thou shalt not take a wife of the daughters of Canaan.",
*            "2": "Arise, go to Padanaram, to the house of Bethuel thy mother's father; and take thee a wife from thence of the daughers of Laban thy mother's brother."
*         }
*         "NKJV": {
*            "1": "Then Isaac called Jacob and blessed him, and [a]charged him, and said to him: “You shall not take a wife from the daughters of Canaan.",
*            "2": "Arise, go to Padan Aram, to the house of Bethuel your mother’s father; and take yourself a wife from there of the daughters of Laban your mother’s brother.",
*            ...
*          }
*      }
* }
* ```
*/
export interface IChaptersResponse {
    status: `${Status}`;
    data: {
        [chapterNumber: string]: {
            [translation: string]: { [verseNumber: string]: string } | null;
        }
    }
}

export class IResponses {
    /**  Pick a (0-based) `from`-`to` range of `translation(s)` to keep, cutting out the excluded ones out of `IChapterResponse.data`  
    * param: `to` is exclusive  
    * *No sanity checks, caller beware.*  */
    static range(from:number, to:number, response:IChapterResponse): IChapterResponse {
        let translations: object[] = [];
        for (const [i, [key, value]] of Object.entries(response.data).entries())
            if(from <= i && i < to)
                translations.push({[key]:value});

        return {
            status: response.status,
            data: Object.assign({}, ...translations)
        }
    }

    /**  Transform an `IChaptersResponse` to an `IChapterResponse`.  
    * No sanity checks, caller beware.  */ 
    static transform(chapter:number, from:IChaptersResponse): IChapterResponse {
        let chapterObject;
        for (const [i, [key, value]] of Object.entries(from.data).entries())
            if(parseInt(key) === chapter)
                chapterObject = value;

        if (Object.values(chapterObject).every(value => value !== null)) {
            return {
                status: Status.Success,
                data: chapterObject
            }
        } else if (Object.values(chapterObject).every(value => value === null)) {
            return {
                status: Status.NotFound,
                data: chapterObject
            }
        } else {
            return {
                status: Status.Partial,
                data: chapterObject
            }
        }
    }
}