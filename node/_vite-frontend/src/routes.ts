export const Routes = {
    Index : '/',
    Report: '/report'
} as const;

export class Router {
    static isAt(route:string) {
        return (window.location.pathname === route)
    }
}