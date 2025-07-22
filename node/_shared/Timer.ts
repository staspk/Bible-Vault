import { printRed, printYellow } from "./print.js";

/**
* Supports both: Browser and Nodejs Environments.
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
            printRed(`Timer.elapsed() called before Timer.start()`);
            return;
        }

        const NOW = performance.now();

        let elapsed = Timer._elapsed.length < 1
            ? NOW - Timer._startTime
            : NOW - Timer._elapsed[Timer._elapsed.length - 1]

        Timer._elapsed.push(NOW);
        
        if (elapsed > 1000) {
            elapsed = elapsed / 1000;
            printYellow(`Operation [${operationName}] timed at: ${elapsed.toFixed(3)}s`)
        } else
            printYellow(`Operation [${operationName}] timed at: ${elapsed.toFixed(3)}ms`)
    }
    
    static stop() {
        if (Timer._startTime == null)
            return;
        
        let elapsed = performance.now() - Timer._startTime;
        if (elapsed > 1000) {
            elapsed = elapsed / 1000;
            printYellow(`Timer total: ${elapsed.toFixed(3)}s`)
        } else
            printYellow(`Timer total: ${elapsed.toFixed(3)}ms`)
        
        Timer._startTime = null;
        Timer._elapsed = []
    }
}