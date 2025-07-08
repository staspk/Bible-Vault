import { ServerResponse } from 'http';

/**
* 400 - Bad Request `{ 'Content-Type': 'application/json' }`
*
* This function is intended to be used when the client provides
* malformed or invalid request parameters.
*
* @returns {void}
*/
export function respondBadRequest(response:ServerResponse, errorMsg = 'Malformed/Invalid Required Query Params'): void {
    response.writeHead(400, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ ok: false, error: errorMsg }));
}


export function handleNotFound(response:ServerResponse, errorMsg = 'Requested resource(s) '): void {
    response.writeHead(404, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ ok: false, error: errorMsg }));
}


export enum Status {
    Success = "success",
    Partial = "partial",
    Error   = "error"
}