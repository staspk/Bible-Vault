import { BIBLE, BibleChaptersIterator, Book } from "../../models/Bible.js"
import { BibleReportApi } from "../../models/BibleReportApi.js";
import { Document, Placeholder } from "../../../kozubenko.ts/Document.js"
import { ContentView } from "../../../index.js";
import { createPopper } from '@popperjs/core';
import type { IReportResponse } from "../../../../_shared/interfaces/IResponses.js";
import { sleep } from "../../../../kozubenko/utils.js";
import { Router, Routes } from "../../routes.js";



const CHAPTERS_PER_ROW = 41;

export class ReportView {
    static ID = 'report-view';
    static Element: HTMLDivElement;
    
    /** Component fetches/constructs only once */
    static Data:IReportResponse;
    static Report:HTMLDivElement;

    public static Render(onto:HTMLElement=ContentView.PlaceHolder()) {
        Document.Title("Data Integrity Report");
        if(!Placeholder.ReplaceWith(onto, ReportView))
            return;

        window.history.pushState({}, '', Routes.Report);

        if(!this.Data) {
            BibleReportApi.Fetch().then(data => {
                if(!data) return;
                this.Data = data;
                if(this.Report) {
                    this.completeRender();
                    this.separateTestaments();
                }
            });
        } else { this.Element.append(this.Report); return; }
        this.Report = this.renderSkeleton();
        
    }

    /** First Step (~57.5ms) */
    static renderSkeleton(): HTMLDivElement {
        const view = Object.assign(document.createElement('div'), {
            id: `${ReportView.ID}-books`
        });
        
        let row = Document('div', { className:'row' }); 
        for (const { i, book, chapter } of BibleChaptersIterator()) {
            row.append(Document('div', {
                id: `ch.${i}`,
                className: 'chapter'
            }));
            row.append(Document('span', {
                className: 'tooltip',
                innerText: `${book.name} ${chapter}`
            }));

            if(i % CHAPTERS_PER_ROW == 0 || i==BIBLE.totalChapters()) {
                view.append(row);
                row = Document('div', { className:'row' });
            }
        }
        ReportView.Element.append(view);

        const chapters = view.querySelectorAll('.chapter');
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

        return view;
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

            if(Number(chapterIndex) % 10 === 0)
                await sleep(1);
        }
    }

    /** Draws a border between the Old/New Testaments */
    static separateTestaments() {
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
    /** `separateTestaments()` Helper */
    static getChapterElements(lower_bound:number, upper_bound:number) {
        let total = upper_bound - lower_bound;
        let elements:HTMLDivElement[] = [];
        for (let i = 0; i < total; i++) {
            elements.push(document.getElementById(`ch.${lower_bound+i}`) as HTMLDivElement)
        }
        return elements;
    }

    static highlightBook(to_highlight:Book|null) {
        if(Router.isAt(Routes.Report)) {
            window.history.pushState({}, '', `?${(to_highlight as Book).name}`);
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
}