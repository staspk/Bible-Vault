import { BIBLE, BibleIterator, Book } from "../../models/Bible.js"
import { ContentView } from "../../../index.js";
import { createPopper } from '@popperjs/core';
import { printGreen, printRed } from "../../../../kozubenko/print.js";
import { Document, Placeholder } from "../../../kozubenko.ts/Document.js"




export class ReportView {
    static ID = 'report-view';
    static Element: HTMLDivElement;
    
    /** Constructed only once, held in memory. */
    static Report: HTMLDivElement;
    static steps_complete = 0; static STEPS_TOTAL = 66;

    public static Render(onto:HTMLElement=ContentView.PlaceHolder()) {
        Document.Title("Data Integrity Report");
        if(!Placeholder.ReplaceWith(onto, ReportView))
            return;

        if(this.Report) {
            this.Element.append(this.Report);
        } else this.Report = this.renderSkeleton();

        if(this.steps_complete < this.STEPS_TOTAL)
            this.renderStep(this.steps_complete++);
    }

    /** Main View (~5ms)  
      includes: contruction, DOM append onto: `ReportView.Element`  */
    static renderSkeleton(): HTMLDivElement {
        const view = Object.assign(document.createElement('div'), {
            id: `${ReportView.ID}-books`
        });

        let row = Document('div', { className:'row' }); 
        const MAX_PER_ROW = 41;

        for (const { i, book, chapter } of BibleIterator()) {
            row.append(Document('div', {
                id: `${book.abbr}-${chapter}`,
                className: 'chapter'
            }));
            row.append(Document('span', {
                className: 'tooltip',
                innerText: `${book.name} ${chapter}`
            }));

            if(i % MAX_PER_ROW == 0 || i==BIBLE.totalChapters()) {
                view.append(row);
                row = Document('div', { className:'row' }); 
            }
        }
        ReportView.Element.append(view);

        const books = view.querySelectorAll('.chapter');
        const tooltips = view.querySelectorAll('.tooltip') as NodeListOf<HTMLElement>;
        for (let index = 0; index < books.length; index++) {
            const popperInstance = createPopper(books[index], tooltips[index], {
                placement: 'top'
            });

            ['mouseenter'].forEach((event) => {
                books[index].addEventListener(event, () => {
                    tooltips[index].style.display = 'block';
                    popperInstance.update();      // We need to tell Popper to update the tooltip position after we show the tooltip, otherwise it will be incorrect
                })
            });
            ['mouseleave'].forEach((event) => {
                books[index].addEventListener(event, () => {
                    tooltips[index].style.display = 'none'
                })
            });
        }
        return view;
    }

    static renderStep(i:number) {
        let z=0;
        while(true) {
            z++;
        }
    }

    /** Secondary View */
    static renderBookView(book:Book): HTMLDivElement {
        const start = performance.now();

        const view = Object.assign(document.createElement('div'), {
            id: ReportView.ID,
        });

        console.log(`renderBook: ${book}`);
        const elapsed = performance.now() - start;
        printGreen(`renderBookView: ${elapsed} ms`);
    }
}




// const popperInstance = createPopper(books, tooltips, {
//     strategy: 'fixed',
//     placement: 'top',
//     modifiers: [
//         {
//             name: 'offset',
//             options: {
//                 offset: [0, 2],
//             },
//         },
//     ],
// })
