import * as http from 'http';


/**
* 204 - No Content (bodyless)
*
* Server successfully processed client’s request but nothing needs to be returned. e.g: POST, PUT, DELETE requests
*/
export function handleNoContent(response:http.ServerResponse, errorMsg = 'Malformed/Invalid Required Query Params'): void {
    response.writeHead(204);
    response.end();
}

/**
* 400 - Bad Request `{ 'Content-Type': 'application/json' }`
*
* Client provided malformed or invalid request parameters.
*/
export function handleBadRequest(response:http.ServerResponse, errorMsg = 'Malformed/Invalid Required Query Params'): void {
    response.writeHead(400, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ ok: false, error: errorMsg }));
}

/**
* 404 - Not Found `{ 'Content-Type': 'application/json' }`
*
* Server could not find the requested resource(s).
*/
export function handleNotFound(response:http.ServerResponse, errorMsg = 'Not Found'): void {
    response.writeHead(404, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ error: errorMsg }));
}


export enum Status {
    Success = "success",
    Partial = "partial",
    Error   = "error"
}