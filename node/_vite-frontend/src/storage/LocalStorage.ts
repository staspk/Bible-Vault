import { BibleApi } from "../models/BibleApi";
import type { ILocalStorageDefaults } from "./ILocalStorageDefaults";
import { LocalStorageKeys } from "./LocalStorageKeys.enum";


export const Defaults: ILocalStorageDefaults = {
    [LocalStorageKeys.MIRROR_OPTION]: true,
    [LocalStorageKeys.TRANSLATIONS]: BibleApi.translationsDefault
}


/** Side-effect load instantiates to `LocalStorage.instance` */
export class LocalStorage {
    static Instance:LocalStorage

    constructor(public defaults:ILocalStorageDefaults = Defaults) {
        if(!LocalStorage.getBoolean("HAVE_LOCAL_STORAGE_DEFAULTS_BEEN_SET?")) {
            LocalStorage.setDefaults(defaults);
            LocalStorage.setBoolean("HAVE_LOCAL_STORAGE_DEFAULTS_BEEN_SET?", true);
        }
        LocalStorage.Instance = this;
    }

    /** Sets `LocalStorage` to `"default"` state, ie:  
    *   - `localStorage.clear();`
    *   - `LocalStorage.setDefaults(LocalStorage.LocalStorageDefaultValues);` */
    resetDefaults(defaults:ILocalStorageDefaults = Defaults) {
        localStorage.clear();
        LocalStorage.setDefaults(defaults);
    }

    static setDefaults(defaults:ILocalStorageDefaults) {
        for (const [key, value] of Object.entries(defaults)) {
            if (typeof value === "string")
                localStorage.setItem(key, value);
            else if (typeof value === "boolean")
                LocalStorage.setBoolean(key, value);
            else if (Array.isArray(value))
                LocalStorage.setArray(key, value);
            else 
                console.error(`LocalStorage.setDefaults(): encountered an unsupported type on key: ${key}`);
        }
    }

    static getArray(key:string) {
        const value = localStorage.getItem(key);
        if (value === null) return null;
        
        return value.split(',').filter(el => el);
    }
    static setArray(key:string, value:Array<string>) {
        localStorage.setItem(key, value.toString());
    }
    
    static toggleBoolean(key:string) {
        const bool = localStorage.getItem(key);
        if (bool === "true")
            localStorage.setItem(key, "false");
        else if (bool === "false")
            localStorage.setItem(key, "true");
        else
            console.error(`LocalStorage.toggleBoolean(${key}): encountered a non-boolean value saved under key. Value: ${bool}`);
    }

    static getBoolean(key:string): boolean|null {
        const bool = localStorage.getItem(key);
        if (bool === "true")  return true;
        if (bool === "false") return false;

        if(bool !== null) 
            console.error(`LocalStorage.getBoolean(${key}): encountered a non-boolean value saved under key. Value: ${bool}`);

        return null;
    }

    /** `value ? localStorage.setItem(key, "true") : localStorage.setItem(key, "false")`  */
    static setBoolean(key:string, value:boolean) {
        value ? localStorage.setItem(key, "true") : localStorage.setItem(key, "false")
    }
    
}

localStorage.clear()
new LocalStorage(Defaults);