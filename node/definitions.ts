import { fileURLToPath } from "url";
import { dirname, resolve } from "path";

const __filename = fileURLToPath(import.meta.url);
const DEFINITIONS_TS = resolve(__filename);

export { DEFINITIONS_TS };