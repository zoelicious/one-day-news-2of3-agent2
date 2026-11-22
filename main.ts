import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

// one-day-news-2of3-agent2 (news-image-20261121): copy the pre-rendered
// 1024x1024 front page into the grader's output directory. Paths resolve
// from this file's location via import.meta.url, never from process.cwd().
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
