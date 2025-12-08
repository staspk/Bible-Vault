import { Document } from "../../../kozubenko.ts/Document.js";
import { Router, Routes } from "../../routes.js";
import { IViewComponent } from "../../../kozubenko.ts/IComponentView.js";
import { createPopper } from '@popperjs/core';
import { BibleChaptersIterator, Book } from "../../models/Bible.js"
import { BibleReportApi } from "../../models/BibleReportApi.js";
import type { IReport, IReportResponse } from "../../../../_shared/interfaces/IResponses.js";
import { ContentView } from "../../../index.js";
import { SearchInput } from "../SearchInput/SearchInput.js";



const CHAPTERS_PER_ROW = 41;
const CSS_COLOR_GRADE_CLASS = (missing_translations_for_chapter:number) => {
    if(missing_translations_for_chapter < 1)      return 'perfect';
    else if(missing_translations_for_chapter < 3) return 'good';
    else if(missing_translations_for_chapter < 6) return 'medium';
    else                                          return 'bad';
}

export class ReportView {
    static ID = 'report-view';
    static Element: HTMLDivElement;
    
    /** Component fetches/constructs only once */
    static Data:IReportResponse;
    static Report:HTMLDivElement;

    static highlightedBook = false;

    public static Render(onto:HTMLElement=ContentView.PlaceHolder()) {
        Document.Title("Data Integrity Report", Routes.Report);
        if(!IViewComponent.ReplaceWith(onto, ReportView))
            return;

        if(this.Data) {
            this.Element.append(this.Report);
            return;
        }
        this.renderSkeleton().then(skeleton => { this.Report = skeleton; });
        BibleReportApi.Fetch().then(data => {
            if(!data) return;
            this.Data = data;
            if(this.Report) {   /* renderSkeleton() => ~60ms. Building report on server => ~240ms. completeRender() should always be succesful */
                this.completeRender();
                SearchInput.Placeholder('highlight Book: Isaiah')
            }
        });
    }
    
    /** injection point from `SearchInput` component. */
    static Highlight(Book:Book) {
        if(Router.isAt(Routes.Report)) {
            const report = this.Report.cloneNode(true) as HTMLDivElement;
            this.Element.children[0].replaceWith(report);

            for (const { i, book, chapter } of BibleChaptersIterator()) {
                if(book !== Book) {
                    const div = document.getElementById(`ch.${i}`) as HTMLDivElement;
                    div.style.opacity = '.4'
                }
            }
            this.highlightedBook = true;
        }
    }
    static Unhighlight() {
        if(this.highlightedBook) {
            this.Element.children[0].replaceWith(this.Report);
            this.highlightedBook = false;
        }
    }

    static chapters:NodeListOf<HTMLDivElement>;
    static tooltips:NodeListOf<HTMLElement>;
    static poppers:any[];
    /** (~60ms) */
    static async renderSkeleton(): Promise<HTMLDivElement> {
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

        this.chapters = view.querySelectorAll('.chapter') as NodeListOf<HTMLDivElement>;
        this.tooltips = view.querySelectorAll('.tooltip') as NodeListOf<HTMLElement>;
        this.poppers = [];
        for (let i = 0; i < this.chapters.length; i++) {
            this.poppers[i] = createPopper(this.chapters[i], this.tooltips[i], {
                placement: 'top'
            });
        }
        view.addEventListener('mouseover', (e) => this.onMouseOverEvents(e));
        view.addEventListener('mouseout',  (e) => this.onMouseOverEvents(e));

        this.draw_borders_between_books(this.chapters);
        this.draw_border_between_Testaments();

        return view;
    }
    static async completeRender() {
        const IDEAL_TRANSLATIONS_FOR_CHAPTER:number = this.Data.translations;
        for (const [chapter, translations_available] of Object.entries(this.Data.report as IReport)) {
            const missing_translations:number = IDEAL_TRANSLATIONS_FOR_CHAPTER - translations_available;
            document.getElementById(`ch.${chapter}`)!.classList.add(
                CSS_COLOR_GRADE_CLASS(missing_translations)
            );
        }
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
            if(i==elements.length-1) elements[i].style.borderRight = '2px solid #495162';
            elements[i].style.borderBottom = '2.5px solid #495162';
        }

        elements = this.getChapterElements(930, 971);
        for (let i = 0; i < elements.length; i++) {
            if(i==0) elements[i].style.borderLeft = '1.7px solid #21252b';
            elements[i].style.borderTop = '2px solid #21252b';
        }

        (document.getElementById(`ch.888`) as HTMLDivElement).style.borderBottomRightRadius = '.2rem';
        (document.getElementById(`ch.971`) as HTMLDivElement).style.borderTopLeftRadius = '.1rem';
    }

    static onMouseOverEvents(event:MouseEvent) {
        const chapter = (event.target as HTMLElement).closest('.chapter');
        if (!chapter || !this.Report.contains(chapter)) return;

        const index = Array.prototype.indexOf.call(this.chapters, chapter);
        if (index === -1) return;

        const tooltip = this.tooltips[index];
        
        if(event.type === 'mouseover') {
            tooltip.style.display = 'block';
            this.poppers[index].update();
        } else tooltip.style.display = 'none';
    }


    static getChapterElements(lower_bound:number, upper_bound:number) {
        let elements:HTMLDivElement[] = [];
        for (let i = lower_bound; i < upper_bound; i++)
            elements.push(document.getElementById(`ch.${i}`) as HTMLDivElement)
        return elements;
    }
}