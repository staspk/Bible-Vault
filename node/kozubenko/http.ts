import { ServerResponse } from 'http';

/**
* 400 - Bad Request `{ 'Content-Type': 'application/json' }`
*
* Intended to be used when the client provides malformed or invalid request parameters.
*/
export function respondBadRequest(response:ServerResponse, errorMsg = 'Malformed/Invalid Required Query Params'): void {
    response.writeHead(400, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ ok: false, error: errorMsg }));
}

/**
* 404 - Not Found `{ 'Content-Type': 'application/json' }`
*
* Intended to be used when the requested resource(s) could not be found.
*/
export function handleNotFound(response:ServerResponse, errorMsg = 'Requested resource(s) '): void {
    response.writeHead(404, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ ok: false, error: errorMsg }));
}


export enum Status {
    Success = "success",
    Partial = "partial",
    Error   = "error"
}