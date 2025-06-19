import * as process from "process";

import { assert_string } from "./utils";



class TerminalColors {
  private constructor() {}  // prevent instantiation

  static readonly Black = "\x1b[30m";
  static readonly DarkBlue = "\x1b[34m";
  static readonly DarkGreen = "\x1b[32m";
  static readonly DarkCyan = "\x1b[36m";
  static readonly DarkRed = "\x1b[31m";
  static readonly DarkMagenta = "\x1b[35m";
  static readonly DarkYellow = "\x1b[33m";
  static readonly Gray = "\x1b[37m";
  static readonly DarkGray = "\x1b[90m";
  static readonly Blue = "\x1b[94m";
  static readonly Green = "\x1b[92m";
  static readonly Cyan = "\x1b[96m";
  static readonly Red = "\x1b[91m";
  static readonly Magenta = "\x1b[95m";
  static readonly Yellow = "\x1b[93m";

  // Currently in Use:
  static readonly White = "\x1b[97m";
  static readonly Reset = "\x1b[0m";
}


/**
 * QoL Function for pretty-printing a variable [var_name as *white*, var_val as *gray*]
 *
 * Example: `print('DEFINITIONS_TS', DEFINITIONS_TS)`;
 */
export function print(var_name:string, var_val:string): void {
  assert_string("var_name", var_name)
  assert_string("var_val", var_val)

  process.stdout.write(`${TerminalColors.White}${var_name}: ${TerminalColors.Reset}${var_val}\n`);
}