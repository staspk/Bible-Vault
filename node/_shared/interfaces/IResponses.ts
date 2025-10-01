import { Status } from "../enums.js";
import { printGreen, printOrange, printYellow } from "../print.js";


export type verseString = string;


/**
* ***EXAMPLE:***
```json
{
    "KJV": null,
    "NKJV": {
      "1": "Now it came to pass, when Isaac was old and his eyes were so dim that he could not see, that he called Esau.",
      "2": "Then he said, “Behold now, I am old. I do not know the day of my death.",
      ...
    },
    "RSV": {
      "1": "This is the book of the generations of Adam. When God created man, he made him in the likeness of God.",
      "2": "Male and female he created them, and he blessed them and named them Man when they were created.",
      ...
    },
    ...
}
```
*/
export interface IChapter {
    [translation: string]: {
        [verseNumber: string]: verseString
    } | null;
}

/**
* ***EXAMPLE:***
```json
{
    "27": {
      "KJV": null,
      "NKJV": {
        "1": "Now it came to pass, when Isaac was old and his eyes were so dim that he could not see, that he called Esau.",
        "2": "Then he said, “Behold now, I am old. I do not know the day of my death.",
        ...
      }
    },
    "28": {
      "KJV": {
        "1": "And Isaac called Jacob, and blessed him, and charged him, and said unto him, Thou shalt not take a wife...",
        "2": "Arise, go to Padanaram, to the house of Bethuel thy mother's father; and take thee a wife from thence...",
        ...
      },
      "NKJV": {
        "1": "Then Isaac called Jacob and blessed him, and [a]charged him, and said to him: “You shall not take a wife...",
        "2": "Arise, go to Padan Aram, to the house of Bethuel your mother’s father; and take yourself a wife...",
        ...
      }
    }
}
```
*/
export interface IChapters {
    [chapter: string]: {
        [translation: string]: {
            [verseNumber: string]: verseString
        } | null;
    }
}

/**
* ***EXAMPLE:***
```json
{
    "status": "success",
    "data": {
      "KJV": null,
      "NKJV": {
        "1": "This is the book of the genealogy of Adam. In the day that God created man, He made him in the likeness of God.",
        "2": "He created them male and female, and blessed them and called them Mankind in the day they were created.",
        ...
      },
      "RSV": {
        "1": "This is the book of the generations of Adam. When God created man, he made him in the likeness of God.",
        "2": "Male and female he created them, and he blessed them and named them Man when they were created.",
        ...
      },
      "NRSV": {
        "1": "This is the list of the descendants of Adam. When God created humans, he made them in the likeness of God.",
        "2": "Male and female he created them, and he blessed them and called them humans when they were created.",
        ...
      },
      "NASB": {
        "1": "This is the book of the generations of Adam. On the day when God created man, He made him in the likeness of God.",
        "2": "He created them male and female, and He blessed them and named them “mankind” on the day when they were created."
        ...
      }
    }
}
```
*/
export interface IChapterResponse {
    status: `${Status}`;
    data: IChapter
}

/**
* ***EXAMPLE:***
```json
{
    "status": "partial",
    "data": {
      "27": {
        "KJV": null,
        "NKJV": {
          "1": "Now it came to pass, when Isaac was old and his eyes were so dim that he could not see, that he called Esau...",
          "2": "Then he said, “Behold now, I am old. I do not know the day of my death.",
          ...
        }
      },
      "28": {
        "KJV": {
          "1": "And Isaac called Jacob, and blessed him, and charged him, and said unto him, Thou shalt not take a wife...",
          "2": "Arise, go to Padanaram, to the house of Bethuel thy mother's father; and take thee a wife from thence...",
          ...
        },
        "NKJV": {
          "1": "Then Isaac called Jacob and blessed him, and [a]charged him, and said to him: “You shall not take a wife...",
          "2": "Arise, go to Padan Aram, to the house of Bethuel your mother’s father; and take yourself a wife...",
          ...
        }
      }
    }
}
```
*/
export interface IChaptersResponse {
    status: `${Status}`;
    data: IChapters
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

    static wrapAsResponse(chapter:IChapter): IChapterResponse {
        let amountNull = 0, total = 0;
        for (const [translation, verses] of Object.entries(chapter))
            if(verses === null)
                amountNull++;
            total++;

        if (amountNull === 0) {
            return {
                status: Status.Success,
                data: chapter
            }
        } else if(total === amountNull) {
            return {
                status: Status.NotFound,
                data: chapter
            }
        } else {
            return {
                status: Status.Partial,
                data: chapter
            }
        }
    }
}