/** values correspond to `URL.pathname` */
export const ApiEndpoints = {
    Passage: '/api/passage',
    Bible_Report: '/api/bible-report',

    isEndpoint(url_pathname:string): boolean {
        return Object.values(ApiEndpoints).includes(url_pathname)
    }
};