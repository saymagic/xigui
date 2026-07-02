import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const dist = path.join(root, "dist");
const entries = ["index.html", ".nojekyll", "src", "assets"];

fs.rmSync(dist, { recursive: true, force: true });
fs.mkdirSync(dist, { recursive: true });

for (const entry of entries) {
  const source = path.join(root, entry);
  const target = path.join(dist, entry);
  fs.cpSync(source, target, { recursive: true });
}

console.log(`Built static site in ${path.relative(root, dist)}`);
