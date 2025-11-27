/** values correspond to `URL.pathname` */
export const ApiEndpoints = {
    Bible: '/api/bible',
    Report: '/api/bible-report',

    isEndpoint(url_pathname:string): boolean {
        return Object.values(ApiEndpoints).includes(url_pathname)
    }
};