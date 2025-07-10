
/**
* Supports both: Browser and Nodejs Environments.
*/
export class Timer {
    static YELLOW_ANSI_CODE = '\x1b[93m';
    static RESET_ANSI_CODE  = '\x1b[0m';

    static isBrowser: boolean = null;
    static startTime: number = null;

    static start() {
        if(Timer.isBrowser == null)
            Timer.isBrowser = typeof window !== 'undefined' && typeof window.document !== 'undefined';

        Timer.startTime = performance.now();
    }
    
    static elapsed(operationName = '') {
        if (!Timer.startTime)
            return;
        
        let elapsed = performance.now() - Timer.startTime;
            if (elapsed > 1000) {
                elapsed = elapsed / 1000;
                Timer.smartPrint(`Operation [${operationName}] timed at: ${elapsed.toFixed(3)}s`);
            } else
                Timer.smartPrint(`Operation [${operationName}] timed at: ${elapsed.toFixed(3)}ms`);
    }
    
    static stop() {
        if (!Timer.startTime)
            return;
        
        let elapsed = performance.now() - Timer.startTime;
        if (elapsed > 1000) {
            elapsed = elapsed / 1000;
            Timer.smartPrint(`Operation timed at: ${elapsed.toFixed(3)}s`);
        } else
            Timer.smartPrint(`Operation timed at: ${elapsed.toFixed(3)}ms`);
        
        Timer.startTime = null;
    }
    
    /**
    * Prints to browser console or process.stdout, depending on environment/runtime.
    */
    static smartPrint(text) {
        if (Timer.isBrowser)
            console.log(`%c${text}`, 'color: yellow');
        else
            process.stdout.write(`${Timer.YELLOW_ANSI_CODE}${text}${Timer.RESET_ANSI_CODE}`);
    }
}