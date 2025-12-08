import * as process from "process";


class TerminalColors {
    private constructor() {}  // prevent instantiation
    
    static readonly Black = "\x1b[30m";
    static readonly DarkBlue = "\x1b[34m";
    static readonly DarkGreen = "\x1b[32m";
    static readonly DarkCyan = "\x1b[36m";
    static readonly DarkRed = "\x1b[31m";
    static readonly DarkMagenta = "\x1b[35m";
    static readonly DarkYellow = "\x1b[33m";
    static readonly DarkGray = "\x1b[90m";
    static readonly Blue = "\x1b[94m";
    static readonly Cyan = "\x1b[96m";
    static readonly Magenta = "\x1b[95m";
    
    // Currently in Use:
    static readonly White = "\x1b[97m";
    static readonly Yellow = "\x1b[93m";
    static readonly Red = "\x1b[91m";
    static readonly Green = "\x1b[92m";
    static readonly Reset = "\x1b[0m";    
}


/**
* QoL Function for pretty-printing a variable [var_name as *white*, var_val as *gray*]
*
* - `print("process.argv", process.argv)` Pretty-Print Variable
* - `print()` prints empty line
*/
export function print(varName?:string, value?:any): void {
    if(!varName && !value) {
        console.log();
        return;
    }
    if (typeof value === "string" || typeof value === "number") {
        process.stdout.write(`${TerminalColors.White}${varName}: ${TerminalColors.Reset}${value}\n`);
        return;
    }
    if (Array.isArray(value)) {
        const joined = value.join(", ");
        process.stdout.write(`${TerminalColors.White}${varName}: ${TerminalColors.Reset}[${joined}]\n`);
        return;
    }
    
    throw new Error("print() not implemented");
}

export class Print {
    static isBrowserConsole = typeof window !== 'undefined' && typeof window.document !== 'undefined';

    static green(text:string, newLine:boolean=true) {
        if(Print.isBrowserConsole)
            console.log(`%c${text}`, 'color: limegreen');
        else {
            process.stdout.write(`${TerminalColors.Green}${text}${TerminalColors.Reset}`);
            if(newLine)
                console.log();
        }
    }

    static red(text:string, newLine:boolean=true) {
        if(Print.isBrowserConsole)
            console.log(`%c${text}`, 'color: red');
        else {
            process.stdout.write(`${TerminalColors.Red}${text}${TerminalColors.Reset}`);
            if(newLine)
                console.log();
        }
    }

    static yellow(text:string, newLine:boolean=true) {
        if(Print.isBrowserConsole) {
            console.log(`%c${text}`, 'color: yellow');
        } else {
            process.stdout.write(`${TerminalColors.Yellow}${text}${TerminalColors.Reset}`);
            if(newLine)
                console.log();
        }
    }

    static orange(text:string, newLine:boolean=true) {
        if(Print.isBrowserConsole) {
            console.log(`%c${text}`, 'color: orange');
        } else {
            process.stdout.write(`${TerminalColors.Yellow}${text}${TerminalColors.Reset}`);
            if(newLine)
                console.log();
        }
    }
}