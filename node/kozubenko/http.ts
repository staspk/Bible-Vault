import * as http from 'http'

/**
 * 400 - Bad Request `{ 'Content-Type': 'application/json' }`
 *
 * This function is intended to be used when the client provides
 * malformed or invalid request parameters.
 *
 * @returns {void}
 */
export function respondBadRequest(response:http.ServerResponse, errorMsg = 'Malformed/Invalid Required Query Params'): void {
    response.writeHead(400, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ error: errorMsg }));
}