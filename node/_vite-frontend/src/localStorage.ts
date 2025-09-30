export enum LocalStorageKeys {
    isFirstVisit = "IS_FIRST_VISIT__LOCAL_STORAGE_KEY",

    /** `PassageView.mirrorOption` */
    mirrorOption = "MIRROR_OPTION__LOCAL_STORAGE_KEY"
}

export class LocalStorage {
    /**  `localStorage=="true"` ? `true` : `false` */
    static getBoolean(key:string):boolean {
        return localStorage.getItem(key)?.toLowerCase() === "true" ? true : false;
    }

    /** `value ? localStorage.setItem(key, "true") : localStorage.setItem(key, "false")`  */
    static setBoolean(key:string, value:boolean) {
        value ? localStorage.setItem(key, "true") : localStorage.setItem(key, "false")
    }
}