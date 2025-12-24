/* 
TESTED [24/12/2025]:
    - Every possible truthy permutation that should return Book (PASS)
    - The 3 forms of input that should return null (PASS)
*/
import { BIBLE, Book } from "../../../_shared/Bible";
import { Print } from "../../../kozubenko/print";
import { BookSearch } from "../models/BookSearch";


function test_search(string:string, expected_book:Book) {
    for (let i = string.length; i >= 0; i--) {
        let book = BookSearch(string);
        if(book === expected_book) Print.green(`${string} search yielded correct Book`)
        else                       Print.red(`${string} search FAILED`)

        string = string.slice(0, i);
    }
}

for (const book of BIBLE.Books()) {
    test_search(book.name, book);
}

let book = BookSearch("Tituss")
if(book === null) Print.green('SEARCH:STRING LONGER THAN POSSIBLE_VALID_SEARCHS YIELDS NULL AS EXPECTED')
else              Print.red('SEARCH:STRING LONGER THAN POSSIBLE_VALID_SEARCHS DOES NOT YIELD NULL!')

book = BookSearch("El")
if(book === null) Print.green('SEARCH:STRING NOT IN POSSIBLE_VALID_SEARCHS YIELDS NULL AS EXPECTED')
else              Print.red('SEARCH:STRING NOT IN POSSIBLE_VALID_SEARCHS DOES NOT YIELD NULL!')

book = BookSearch("x")
if(book === null) Print.green('SEARCH:STRING NOT IN POSSIBLE_VALID_SEARCHS YIELDS NULL AS EXPECTED')
else              Print.red('SEARCH:STRING NOT IN POSSIBLE_VALID_SEARCHS DOES NOT YIELD NULL!')