import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";

const root = process.cwd();
const dist = path.join(root, "dist");
const remote = execFileSync("git", ["remote", "get-url", "origin"], { encoding: "utf8" }).trim();
const temp = fs.mkdtempSync(path.join(os.tmpdir(), "xigui-gh-pages-"));

function run(command, args, cwd = temp) {
  execFileSync(command, args, { cwd, stdio: "inherit" });
}

if (!fs.existsSync(path.join(dist, "index.html"))) {
  throw new Error("dist/index.html not found. Run npm run build first.");
}

fs.cpSync(dist, temp, { recursive: true });
run("git", ["init", "-b", "gh-pages"]);
run("git", ["config", "user.name", "Codex"]);
run("git", ["config", "user.email", "codex@local"]);
run("git", ["add", "."]);
run("git", ["commit", "-m", "Deploy static site to gh-pages"]);
run("git", ["push", remote, "gh-pages:gh-pages", "--force"]);

console.log("Published dist to gh-pages.");
