/** Assumes Node represents a step in a search string path */
export class TreeNode {
    constructor(
        public char:string,
        public depth = 0,
        public children:TreeNode[] = []
    ){}
}

export class Tree {
    static From(list:string[]): TreeNode {
        const root = new TreeNode(list[0][0]);              /* Assumes first character of every string is the same */

        let node = root;
        list.forEach(word => {
            for (let i = 1; i < word.length; i++) {
                let char = word[i];
                if(char) {
                    node = Tree.walk(root, word.slice(1, i));

                    let child = new TreeNode(char, i);
                    if(!node.children.find(node => node.char === char))
                        node.children.push(child);
                }
            }
            node = root;
        });

        return root;
    }

    /** Assumes: caller guarantees that root has a path using str */
    static walk(root:TreeNode, str:string): TreeNode {
        if(!str) return root;

        let node = root;
        for (const char of str)
            node = node.children?.find(node => node.char === char) as TreeNode;

        return node;
    }
}