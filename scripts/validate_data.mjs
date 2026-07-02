import fs from "node:fs";

const payload = JSON.parse(fs.readFileSync("src/data/questions.json", "utf8"));
const failures = [];

if (payload.count !== 393) {
  failures.push(`Expected payload count 393, got ${payload.count}`);
}

if (payload.questions.length !== 393) {
  failures.push(`Expected 393 questions, got ${payload.questions.length}`);
}

const ids = new Set();
const numbers = new Set();
for (const question of payload.questions) {
  if (!question.id || ids.has(question.id)) {
    failures.push(`Duplicate or empty id: ${question.id}`);
  }
  ids.add(question.id);
  numbers.add(question.number);

  for (const field of ["chapter", "question", "answer"]) {
    if (!String(question[field] || "").trim()) {
      failures.push(`Question ${question.id} has empty ${field}`);
    }
  }
}

for (let number = 1; number <= 393; number += 1) {
  if (!numbers.has(number)) {
    failures.push(`Missing global question number ${number}`);
  }
}

for (const chapter of payload.chapters) {
  const count = payload.questions.filter(
    (question) => question.number >= chapter.start && question.number <= chapter.end,
  ).length;
  if (count !== chapter.count) {
    failures.push(`${chapter.title} expected ${chapter.count}, got ${count}`);
  }
}

if (failures.length > 0) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log(`Validated ${payload.questions.length} questions across ${payload.chapters.length} chapters.`);
