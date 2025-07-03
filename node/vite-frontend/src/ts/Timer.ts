
/**
 * For browser JavaScript. `Timer.start()`. `Timer.stop()`
 */
export class Timer {
    static startTime = null;

    static start() {
        Timer.startTime = performance.now();
    }

    static elapsed(timedOperationTitle = '') {
        if (!Timer.startTime)
            return;

        let elapsed = performance.now() - Timer.startTime;
        if (elapsed > 1000) {
            elapsed = elapsed / 1000;
            console.log(`%cOperation timed at: ${elapsed.toFixed(3)}s`, 'color: yellow');
        } else {
            console.log(`%cOperation timed at: ${elapsed.toFixed(3)}ms`, 'color: yellow');
        }
    }

    static stop() {
        if (!Timer.startTime)
            return;
        
        let elapsed = performance.now() - Timer.startTime;
        console.log(`%cOperation timed at: ${elapsed}`, 'color: yellow');

        if (elapsed > 1000) {
            elapsed = elapsed / 1000;
            console.log(`%cOperation timed at: ${elapsed.toFixed(3)}s`, 'color: yellow');
        } else {
            console.log(`%cOperation timed at: ${elapsed.toFixed(3)}ms`, 'color: yellow');
        }

        Timer.startTime = null;
    }
}