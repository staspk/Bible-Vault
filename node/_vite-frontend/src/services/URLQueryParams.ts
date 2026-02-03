import { BibleTranslations as SupportedBibleTranslations, type Translation } from "../../../_shared/BibleTranslations";


/** **EQUIVALENT TO:**
```ts
const urlParams = new URLSearchParams(window.location.search);
return urlParams.get(key);
```
*/
export function UrlParam(key:string): string|null {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(key);
}

/** Returns the expected return value (or null). If you need a naked, untouched `URLSearchParams`, use: `UrlParam()`.  */
export class URLQueryParams {

    static translations(): Translation[] | null {
        const translations = UrlParam('translations')?.split(',').filter(el => el);
        if(!translations)
            return null;

        const BibleTranslations = new Set(
            Object.values(SupportedBibleTranslations)
        );

        /* Removing from translations any value not in BibleTranslations */
        for(let i = 0; i < translations.length; i++) {
            if(!BibleTranslations.has(translations[i])) {
                translations.splice(i, 1);
                i--;
            }
        }
        if(translations.length > 0) {
            return translations as Translation[];
        }

        return null;
        // LocalStorage.getArray(LocalStorageKeys.TRANSLATIONS) as string[]
    }
}