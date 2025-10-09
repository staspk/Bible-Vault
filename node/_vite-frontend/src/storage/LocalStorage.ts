import type { ILocalStorageDefaultValues } from "./ILocalStorageDefaultValues";
import { LocalStorageKeys } from "./LocalStorageKeys.enum";


export class LocalStorage {

    static LocalStorageDefaultValues: ILocalStorageDefaultValues = {
        [LocalStorageKeys.mirrorOption]: false
    };
    
    /** Sets `LocalStorage` to `"default"` state, ie:  
    *   - `localStorage.clear();`
    *   - `LocalStorage.setDefaults(LocalStorage.LocalStorageDefaultValues);` */
    static FirstVisit() {
        localStorage.clear();
        LocalStorage.setDefaults(LocalStorage.LocalStorageDefaultValues);
    }

    static setDefaults(defaults:ILocalStorageDefaultValues) {
        for (const [key, value] of Object.entries(defaults)) {
            console.log(`${key} typeof: ${typeof key}`)

            if (typeof value === "boolean")
                LocalStorage.setBoolean(key, value);
            else if (typeof value === "string")  
                localStorage.setItem(key, value);
            else 
                console.error('LocalStorage.setDefaults(): encountered an unsupported type')
        }
    }
    
    /**  `localStorage=="true"` ? `true` : `false` */
    static getBoolean(key:string):boolean {
        return localStorage.getItem(key)?.toLowerCase() === "true" ? true : false;
    }
    
    /** `value ? localStorage.setItem(key, "true") : localStorage.setItem(key, "false")`  */
    static setBoolean(key:string, value:boolean) {
        value ? localStorage.setItem(key, "true") : localStorage.setItem(key, "false")
    }

    static toggleBoolean(key:string) {
        LocalStorage.getBoolean(key) ? localStorage.setItem(key, "false") : localStorage.setItem(key, "true");
    }
}