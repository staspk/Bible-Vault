


export class ArrayLike {
    /**
    Creates a 1-based Array-Like Object, useful for jsons

    ***EXAMPLE:***
    ```json
    {
        "1": any|null,
        "2": any|null,
        "3": any|null,
    }
    ```
    */
    static Object(values:any[]) {
        const pojo = {};
        for (let i = 1; i <= values.length; i++)
            pojo[i] = values[i-1];
        return pojo;
    }
}