import { Print } from "./print.js";

/** Supports both: Browser and Nodejs Environments.

const START = performance.now();
- {OPERATION} -
let elapsed = performance.now() - START;
if (elapsed > 1000) {
    elapsed = elapsed / 1000;
    Print.green(`Timer total: ${elapsed.toFixed(3)}s`)
} else Print.green(`Timer total: ${elapsed.toFixed(3)}ms`)

*/
export class Timer {
    static isBrowser: boolean = null;
    static _startTime: number = null;
    static _elapsed: number[] = [];
    
    static start() {
        if(Timer.isBrowser == null)
            Timer.isBrowser = typeof window !== 'undefined' && typeof window.document !== 'undefined';
        
        Timer._startTime = performance.now();
    }

    /**  Use to time certain operations. Uses `Timer._startTime` on first call, `Timer._elapsed` on every successive call to determine operation time.  */
    static elapsed(operationName) {
        if (Timer._startTime == null) {
            Print.red(`Timer.elapsed() called before Timer.start()`);
            return;
        }

        const NOW = performance.now();

        let elapsed = Timer._elapsed.length < 1
            ? NOW - Timer._startTime
            : NOW - Timer._elapsed[Timer._elapsed.length - 1]

        Timer._elapsed.push(NOW);
        
        if (elapsed > 1000) {
            elapsed = elapsed / 1000;
            Print.yellow(`Operation [${operationName}] timed at: ${elapsed.toFixed(3)}s`)
        } else
            Print.yellow(`Operation [${operationName}] timed at: ${elapsed.toFixed(3)}ms`)
    }
    
    static stop() {
        if (Timer._startTime == null)
            return;
        
        let elapsed = performance.now() - Timer._startTime;
        if (elapsed > 1000) {
            elapsed = elapsed / 1000;
            Print.yellow(`Timer total: ${elapsed.toFixed(3)}s`)
        } else
            Print.yellow(`Timer total: ${elapsed.toFixed(3)}ms`)
        
        Timer._startTime = null;
        Timer._elapsed = []
    }
}