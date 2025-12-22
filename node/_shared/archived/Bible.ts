class Bible {
    /** A grouping originally planned for a ReportView. Not currently used, but left for posterity.  
        - Torah
        - History
        - Poetry/Wisdom
        - Major Prophets
        - Minor
        - Gospels/Acts
        - Paul
        - Jesus' Inner Circle
    */
    static Categorized(): Book[][] {
        const SEPARATORS = [5, 12, 5, 5, 12, 5, 14, 8]

        let list:Book[][] = []
        let category:Book[] = []
        let offset = 0;
        BIBLE.Books().forEach(book => {
            if(category.push(book) == SEPARATORS[offset]) {
                list.push(category);
                category = [];
                offset++;
            }
        });

        return list;
    }
}