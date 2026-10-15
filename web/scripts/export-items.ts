// Writes the AI-side feed to <repo>/data: items.jsonl, skills.json, techniques.json.
// Run with `npm run items:export` from web/ (uses tsx with the react-server
// condition so the server-only guard on content/items.ts is a no-op).
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { listItems } from "../content/items";
import { listTechniques } from "../content/techniques";
import { itemsToJsonl, skillsExport, techniquesExport } from "../lib/export/items";

const outDir = resolve(process.argv[2] ?? resolve(__dirname, "../../data"));
mkdirSync(outDir, { recursive: true });

const items = listItems();
const techniques = listTechniques();
writeFileSync(resolve(outDir, "items.jsonl"), itemsToJsonl(items));
writeFileSync(resolve(outDir, "skills.json"), JSON.stringify(skillsExport(), null, 2) + "\n");
writeFileSync(resolve(outDir, "techniques.json"), JSON.stringify(techniquesExport(techniques), null, 2) + "\n");

const verified = items.filter((i) => i.desmos?.verified).length;
console.log(`Wrote ${items.length} items (${verified} verified, ${items.length - verified} draft), ${skillsExport().skills.length} skills, ${techniques.length} techniques to ${outDir}`);
