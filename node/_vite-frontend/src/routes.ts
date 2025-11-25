export const Routes = {
    Index : '/',
    Report: '/report'
}


export class Router {
    static isAt(route:string) {
        return (window.location.pathname === route)
    } 
}