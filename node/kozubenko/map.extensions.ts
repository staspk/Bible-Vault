/** Wrapper function to extend: `Map<any,List>` */
export function ListMap(map): ListMap.ListMap {
    return new ListMap.ListMap(map)
}

export namespace ListMap {
    export class ListMap {
        constructor(
            public map:Map<any,any>
        ){}

        Add(key, value) {
            let _value = this.map.get(key);
            if(_value) {
                _value.push(value);
                this.map.set(key, _value)
                return;
            }
            this.map.set(key, [value]);
        }
    }
}
