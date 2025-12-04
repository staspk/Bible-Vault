import { BIBLE, BibleChaptersIterator, Book } from "../../models/Bible.js"
import { BibleReportApi } from "../../models/BibleReportApi.js";
import { Document } from "../../../kozubenko.ts/Document.js";
import { IViewComponent } from "../../../kozubenko.ts/IComponentView.js";
import { ContentView } from "../../../index.js";
import { createPopper } from '@popperjs/core';
import type { IReportResponse } from "../../../../_shared/interfaces/IResponses.js";
import { sleep } from "../../../../kozubenko/utils.js";
import { Router, Routes } from "../../routes.js";
import { printGreen } from "../../../../kozubenko/print.js";



const CHAPTERS_PER_ROW = 41;

export class ReportView {
    static ID = 'report-view';
    static Element: HTMLDivElement;
    
    /** Component fetches/constructs only once */
    static Data:IReportResponse;
    static Report:HTMLDivElement;

    public static Render(onto:HTMLElement=ContentView.PlaceHolder()) {
        window.history.pushState({}, '', Routes.Report);
        Document.Title("Data Integrity Report");
        if(!IViewComponent.ReplaceWith(onto, ReportView))
            return;

        if(!this.Data) {
            BibleReportApi.Fetch().then(data => {
                if(!data) return;
                this.Data = data;
                if(this.Report) {
                    this.completeRender();
                }
            });
        } else { this.Element.append(this.Report); return; }
        this.Report = this.renderSkeleton();
    }

    static highlightBook(to_highlight:Book|null) {
        if(Router.isAt(Routes.Report)) {
            // window.history.pushState({}, '', `?${(to_highlight as Book).name}`);
            const report = this.Report.cloneNode(true) as HTMLDivElement;
            this.Element.children[0].replaceWith(report);
            
            for (const { i, book, chapter } of BibleChaptersIterator()) {
                if(book !== to_highlight) {
                    const el = document.getElementById(`ch.${i}`) as HTMLDivElement;
                    el.style.opacity = '.4'
                }
            }
        }
    }
    static unhighlight() {
        this.Element.children[0].replaceWith(this.Report);
    }

    static async completeRender() {
        const IDEAL_TRANSLATIONS = this.Data.translations;
        for (const [chapterIndex, total_translations] of Object.entries(this.Data.report)) {
            const missing = IDEAL_TRANSLATIONS - total_translations;
            const el = document.getElementById(`ch.${chapterIndex}`) as HTMLDivElement;
            
            if(missing < 1)      el.classList.add('perfect');
            else if(missing < 3) el.classList.add('good');
            else if(missing < 6) el.classList.add('medium');
            else                 el.classList.add('bad');

            if(Number(chapterIndex) % 20 === 0)
                await sleep(1);
        }
    }
    /** (~60ms) */
    static renderSkeleton(): HTMLDivElement {
        const START = performance.now();
        const view = Object.assign(document.createElement('div'), {
            id: `${ReportView.ID}-books`
        });
        
        let row = Document('div', { className:'row' }); 
        for (const { i, book, chapter } of BibleChaptersIterator()) {
            const chapterDiv = Document('div', {
                id: `ch.${i}`,
                className: 'chapter'
            })
            row.append(chapterDiv);
            row.append(Document('span', {
                className: 'tooltip',
                innerText: `${book.name} ${chapter}`
            }));

            chapterDiv.setAttribute('book', book.toString());
            chapterDiv.setAttribute('chapter', chapter.toString());

            if(i % CHAPTERS_PER_ROW == 0) {
                view.append(row);
                row = Document('div', { className:'row' });
            }
        }
        ReportView.Element.append(view);

        const chapters = view.querySelectorAll('.chapter') as NodeListOf<HTMLDivElement>;
        const tooltips = view.querySelectorAll('.tooltip') as NodeListOf<HTMLElement>;
        const poppers: any[] = [];
        for (let i = 0; i < chapters.length; i++) {
            poppers[i] = createPopper(chapters[i], tooltips[i], {
                placement: 'top'
            });
        }
        ['mouseover', 'mouseout'].forEach(event => {
            view.addEventListener(event, (e) => {
                const chapter = (e.target as HTMLElement).closest('.chapter');
                if (!chapter || !view.contains(chapter)) return;

                const index = Array.prototype.indexOf.call(chapters, chapter);
                if (index === -1) return;

                const tooltip = tooltips[index];

                if(event === 'mouseover') {
                    tooltip.style.display = 'block';
                    poppers[index].update();
                } else tooltip.style.display = 'none';
            });
        });

        this.draw_borders_between_books(chapters);
        this.draw_border_between_Testaments();

        let elapsed = performance.now() - START;
        if (elapsed > 1000) {
            elapsed = elapsed / 1000;
            printGreen(`Timer total: ${elapsed.toFixed(3)}s`)
        } else printGreen(`Timer total: ${elapsed.toFixed(3)}ms`)

        return view;
    }

    static draw_borders_between_books(chapters:NodeListOf<HTMLDivElement>) {
        chapters.forEach((chapter, i) => {
            /* has North neighbor */
            if(i > 41) {
                if(chapter.getAttribute('book') !== chapters[i-41].getAttribute('book')) {
                    chapter.style.borderTop = '1px dashed #49516277';
                }
            }
            /* has East neighbor */
            if(!(i%41 === 0) && i !== chapters.length-1) {
                if(chapter.getAttribute('book') !== chapters[i+1].getAttribute('book')) {
                    chapter.style.borderRight = "1px dashed #49516277";
                }
            }
        });
    }
    /** ie: Old/New Testaments */
    static draw_border_between_Testaments() {
        let elements = this.getChapterElements(889, 930);
        for (let i = 0; i < elements.length; i++) {
            if(i==elements.length-1) elements[i].style.borderRight = '3px solid #495162';
            elements[i].style.borderBottom = '3px solid #495162';
        }

        elements = this.getChapterElements(930, 971);
        for (let i = 0; i < elements.length; i++) {
            if(i==0) elements[i].style.borderLeft = '2px solid #21252b';
            elements[i].style.borderTop = '2px solid #21252b';
        }

        (document.getElementById(`ch.888`) as HTMLDivElement).style.borderBottomRightRadius = '.2rem';
        (document.getElementById(`ch.971`) as HTMLDivElement).style.borderTopLeftRadius = '.1rem';
    }


    static getChapterElements(lower_bound:number, upper_bound:number) {
        let elements:HTMLDivElement[] = [];
        for (let i = lower_bound; i < upper_bound; i++)
            elements.push(document.getElementById(`ch.${i}`) as HTMLDivElement)
        return elements;
    }
}