#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CHAPTERS = [
    ("第12章", 1, 102, "第12章 信息系统服务管理"),
    ("第13章", 103, 133, "第13章 人员管理"),
    ("第14章", 134, 145, "第14章 规范与过程管理"),
    ("第15章", 146, 176, "第15章 技术与研发管理"),
    ("第16章", 177, 196, "第16章 资源与工具管理"),
    ("第17章", 197, 200, "第17章 信息系统项目管理"),
    ("第11章", 201, 208, "第11章 信息系统治理"),
    ("第4章", 209, 243, "第4章 信息系统规划"),
    ("第5章", 244, 279, "第5章 应用系统规划"),
    ("第6章", 280, 294, "第6章 云资源规划"),
    ("第7章", 295, 301, "第7章 网络环境规划"),
    ("第8章", 302, 324, "第8章 数据资源规划"),
    ("第9章", 325, 336, "第9章 信息安全规划"),
    ("第10章", 337, 339, "第10章 云原生系统规划"),
    ("第18章", 340, 354, "第18章 智慧城市发展规划"),
    ("第19章", 355, 361, "第19章 智慧园区发展规划"),
    ("第20章", 362, 369, "第20章 数字乡村发展规划"),
    ("第21章", 370, 378, "第21章 企业数字化转型发展规划"),
    ("第22章", 379, 384, "第22章 智能制造发展规划"),
    ("第23章", 385, 393, "第23章 新型消费系统规划"),
]

QUESTION_MARKER_RE = re.compile(r"[【\[]\s*问题\s*(\d+)\s*[】\]J]?\s*")
ANSWER_RE = re.compile(r"^[{｛\[]?\s*[答荅]\s*[}｝\]）)]?\s*[:：]?\s*(.*)")
TIP_RE = re.compile(r"[【\[]\s*(口诀|关键词)\s*[:：]?\s*(.*?)\s*[】\]]")
CHAPTER_RE = re.compile(r"第\s*(\d+)\s*章")
CHAPTER_BY_KEY = {key: {"start": start, "end": end, "title": title} for key, start, end, title in CHAPTERS}

NOISE_PATTERNS = [
    re.compile(r"江山老师"),
    re.compile(r"软考.*老师"),
    re.compile(r"QQ/VX"),
    re.compile(r"关注.*视频号"),
    re.compile(r"案例、论文必背"),
    re.compile(r"2025\s*年系规"),
    re.compile(r"^目录$"),
    re.compile(r"^-\s*\d+\s*-$"),
    re.compile(r"^\d{6,}$"),
]


def clean_text(text: str) -> str:
    replacements = {
        "｛": "{",
        "｝": "}",
        "（": "(",
        "）": ")",
        "﹣": "-",
        "一": "一",
        "、 ": "、",
        "： ": "：",
        " ,": ",",
        " 。": "。",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace(" {答}", "{答}")
    return text


def is_noise(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    return any(pattern.search(stripped) for pattern in NOISE_PATTERNS)


def line_sort_key(line: dict) -> tuple[int, int, float, float]:
    # Vision coordinates are normalized with origin at the bottom left.
    # Most pages are two columns; process left column top-down, then right.
    x = float(line["x"])
    y = float(line["y"])
    column = 0 if x < 0.49 else 1
    return (int(line["page"]), column, -y, x)


def expand_merged_question_lines(lines: list[dict]) -> list[dict]:
    expanded: list[dict] = []
    for line in lines:
        text = str(line["text"])
        matches = list(QUESTION_MARKER_RE.finditer(text))
        if not matches or (len(matches) == 1 and matches[0].start() == 0):
            expanded.append(line)
            continue

        if matches[0].start() > 0:
            prefix = dict(line)
            prefix["text"] = text[: matches[0].start()].strip()
            if prefix["text"]:
                expanded.append(prefix)

        for index, match in enumerate(matches):
            next_start = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            segment_text = text[match.start() : next_start].strip()
            if not segment_text:
                continue
            segment = dict(line)
            segment["text"] = segment_text
            if float(line["x"]) < 0.49 and (index > 0 or match.start() > 0):
                segment["x"] = 0.52
            expanded.append(segment)

    return expanded


def chapter_for(number: int) -> str:
    for _, start, end, title in CHAPTERS:
        if start <= number <= end:
            return title
    return "未分类"


def chapter_key_from_line(line: str) -> str | None:
    match = CHAPTER_RE.search(line)
    if not match:
        return None
    key = f"第{int(match.group(1))}章"
    return key if key in CHAPTER_BY_KEY else None


def strip_question_prefix(line: str) -> tuple[int | None, str]:
    match = QUESTION_MARKER_RE.search(line)
    if not match:
        return None, line
    number = int(match.group(1))
    text = line[match.end() :].strip()
    text = re.sub(r"^[★太*＊\s]+", "", text)
    return number, text


def normalize_answer_lines(lines: list[str]) -> tuple[list[str], str, str, list[str]]:
    pre_answer_parts: list[str] = []
    answer_parts: list[str] = []
    tips: list[str] = []
    raw_parts: list[str] = []
    in_answer = False

    for line in lines:
        line = clean_text(line)
        if is_noise(line):
            continue

        tip_match = TIP_RE.search(line)
        if tip_match:
            label = tip_match.group(1)
            value = tip_match.group(2).strip()
            if value:
                tips.append(f"{label}：{value}")
            line = TIP_RE.sub("", line).strip()
            if not line:
                continue

        answer_match = ANSWER_RE.match(line)
        if answer_match:
            in_answer = True
            rest = answer_match.group(1).strip()
            if rest:
                answer_parts.append(rest)
                raw_parts.append(rest)
            continue

        if in_answer:
            answer_parts.append(line)
            raw_parts.append(line)
        else:
            pre_answer_parts.append(line)
            raw_parts.append(line)

    answer = "\n".join(answer_parts).strip()
    tip = "\n".join(dict.fromkeys(tips)).strip()
    return pre_answer_parts, answer, tip, raw_parts


def parse_questions(lines: list[dict]) -> list[dict]:
    sorted_lines = sorted(expand_merged_question_lines(lines), key=line_sort_key)
    records: list[dict] = []
    current: dict | None = None
    current_chapter_key = "第12章"

    def close_current() -> None:
        nonlocal current
        if current:
            records.append(current)
            current = None

    def append_body(text: str, page: int) -> None:
        if current:
            if page not in current["pages"]:
                current["pages"].append(page)
            current["bodyLines"].append(text)

    for line in sorted_lines:
        text = clean_text(str(line["text"]))
        if is_noise(text):
            continue
        page = int(line["page"])

        chapter_key = chapter_key_from_line(text)
        if chapter_key and (current or records):
            current_chapter_key = chapter_key
            # Chapter heading lines are structural, not answer content.
            text = CHAPTER_RE.sub("", text).strip(" -.。")
            if not text:
                continue

        matches = list(QUESTION_MARKER_RE.finditer(text))
        if matches:
            if matches[0].start() > 0:
                append_body(text[: matches[0].start()].strip(), page)
            for index, match in enumerate(matches):
                close_current()
                next_start = matches[index + 1].start() if index + 1 < len(matches) else len(text)
                local_number = int(match.group(1))
                question_text = text[match.end() : next_start].strip()
                question_text = re.sub(r"^[★太*＊\s]+", "", question_text)
                current = {
                    "chapterKey": current_chapter_key,
                    "localNumber": local_number,
                    "question": question_text,
                    "bodyLines": [],
                    "pages": [page],
                }
            continue

        append_body(text, page)

    close_current()

    questions: list[dict] = []
    seen: set[tuple[str, int]] = set()
    for record in records:
        chapter_key = record["chapterKey"]
        local_number = int(record["localNumber"])
        identity = (chapter_key, local_number)
        if identity in seen:
            continue
        seen.add(identity)

        chapter = CHAPTER_BY_KEY[chapter_key]
        number = chapter["start"] + local_number - 1

        question = clean_text(record["question"])
        pre_answer, answer, tip, raw_parts = normalize_answer_lines(record["bodyLines"])
        if pre_answer and answer:
            question = clean_text(" ".join([question, *pre_answer]))
        elif pre_answer and not answer:
            remaining = list(pre_answer)
            while remaining and "?" not in question and "？" not in question:
                head = remaining[0]
                if len(head) > 24 or re.match(r"^\d+[.、]", head):
                    break
                question = clean_text(" ".join([question, remaining.pop(0)]))
            answer = "\n".join(remaining).strip()
        question = re.sub(r"^[★太*＊\s]+", "", question).strip()

        questions.append(
            {
                "id": f"q{number:03d}",
                "number": number,
                "chapterQuestionNumber": local_number,
                "chapter": chapter["title"],
                "question": question,
                "answer": answer,
                "tip": tip,
                "pages": sorted(record["pages"]),
                "raw": "\n".join(raw_parts).strip(),
            }
        )

    return sorted(questions, key=lambda item: item["number"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ocr_json", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    lines = json.loads(args.ocr_json.read_text(encoding="utf-8"))
    questions = parse_questions(lines)
    payload = {
        "source": "2025年系规-案例论文必背300问.pdf",
        "generatedBy": "macOS Vision OCR",
        "expectedCount": 393,
        "count": len(questions),
        "chapters": [
            {"key": key, "title": title, "start": start, "end": end, "count": end - start + 1}
            for key, start, end, title in CHAPTERS
        ],
        "questions": questions,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    missing = sorted(set(range(1, 394)) - {item["number"] for item in questions})
    empty_answers = [item["number"] for item in questions if not item["answer"]]
    report = [
        f"Parsed questions: {len(questions)}",
        f"Missing numbers: {missing}",
        f"Empty answers: {empty_answers[:40]}{'...' if len(empty_answers) > 40 else ''}",
    ]
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))


if __name__ == "__main__":
    main()
