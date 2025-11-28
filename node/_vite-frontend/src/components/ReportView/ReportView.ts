import { BIBLE, BibleChaptersIterator } from "../../models/Bible.js"
import { BibleReportApi } from "../../models/BibleReport.js";
import { Document, Placeholder } from "../../../kozubenko.ts/Document.js"
import { ContentView } from "../../../index.js";
import { createPopper } from '@popperjs/core';
import type { IReport } from "../../../../_shared/interfaces/IResponses.js";


const Grade = {
    Perfect: '0 missing',
    Good:    '1-2 missing',
    Medium:  '3-5 missing',
    Bad:     '6-10 missing'
} as const;

const CHAPTERS_PER_ROW = 41;

export class ReportView {
    static ID = 'report-view';
    static Element: HTMLDivElement;
    
    /** Component fetches/constructs once */
    static Data:IReport;
    static Report:HTMLDivElement;

    public static async Render(onto:HTMLElement=ContentView.PlaceHolder()) {
        Document.Title("Data Integrity Report");
        if(!Placeholder.ReplaceWith(onto, ReportView))
            return;

        if(this.Report) { this.Element.append(this.Report); return; }

        if(!this.Data) {
            const data = await BibleReportApi.Fetch();
            if(!data) return;
            this.Data = data;
        }
        this.completeRender();
    }

    /** First Step (~57.5ms) */
    static renderSkeleton(): HTMLDivElement {
        const view = Object.assign(document.createElement('div'), {
            id: `${ReportView.ID}-books`
        });
        
        let row = Document('div', { className:'row' }); 
        for (const { i, book, chapter } of BibleChaptersIterator()) {
            row.append(Document('div', {
                id: `${book.abbr}-${chapter}`,
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
        console.log(this.Data);
    }
}