import { BIBLE, Book } from "../../models/Bible.js"
import { ContentView } from '../../../index.js';
import { isNullOrUndefined } from "../../../../kozubenko/utils.js";
import { createPopper } from '@popperjs/core';
import { printGreen, printRed } from "../../../../kozubenko/print.js";


export class ReportView {
    static ID = 'report-view';
    static Element: HTMLDivElement;
    /** Main View */
    static BooksView: HTMLDivElement;   // constructed only once

    public static Render(onto:HTMLElement=ContentView.PlaceHolder()) {
        if(isNullOrUndefined(onto)) {
            console.error('ReportView.Render(): onto is null/undefined. Cannot complete Render...');
            return;
        }
        const reportView = Object.assign(document.createElement('div'), {
            id: ReportView.ID
        }); onto.replaceWith(reportView);
        ReportView.Element = reportView;

        if(ReportView.BooksView) {
            ReportView.Element.append(this.BooksView)
        } else this.BooksView = ReportView.renderBooksView()
    }

    /** Main View (~5ms)  
      includes: contruction, DOM append onto: `ReportView.Element`  */
    static renderBooksView(): HTMLDivElement {
        const view = Object.assign(document.createElement('div'), {
            id: `${ReportView.ID}-books`
        });

        for(const category of BIBLE.Categorized()) {
            const column = Object.assign(document.createElement('div'), {
                className: 'column'
            });

            const books = Object.assign(document.createElement('div'), {
                className: 'books'
            });

            for(const book of category) {
                books.append(Object.assign(document.createElement('div'), {
                    id: book.name,
                    className: 'book',
                    onclick: (e: MouseEvent) => ReportView.renderBookView(book)
                }));

                books.append(Object.assign(document.createElement('span'), {
                    className: 'tooltip',
                    innerText: book.name
                }));
            }
            column.append(books)
            view.append(column)
        }
        ReportView.Element.append(view);

        const books = view.querySelectorAll('.book');
        const tooltips = view.querySelectorAll('.tooltip') as NodeListOf<HTMLElement>;
        for (let index = 0; index < books.length; index++) {
            const popperInstance = createPopper(books[index], tooltips[index], {
                placement: 'top'
            });

            ['mouseenter', 'focus'].forEach((event) => {
                books[index].addEventListener(event, () => {
                    tooltips[index].style.display = 'block';
                    popperInstance.update();      // We need to tell Popper to update the tooltip position after we show the tooltip, otherwise it will be incorrect
                })
            });
            ['mouseleave', 'blur'].forEach((event) => {
                books[index].addEventListener(event, () => {
                    tooltips[index].style.display = 'none'
                })
            });
        }
        return view;
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
