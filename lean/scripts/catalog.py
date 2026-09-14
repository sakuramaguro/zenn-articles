#!/usr/bin/env python3
"""Validate the reviewed inventory against the manuscript, then optionally extract it."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
BOOK = REPO / "books/lean4-formalization"
CATALOG = ROOT / "catalog/index.json"
LABELS = {
    "complete": "完成例・実行コマンド",
    "fragment": "前後に続く断片",
    "expected_error": "意図的なエラー例",
    "unfinished": "練習問題・未完成の骨格",
    "excerpt": "説明用の抜粋",
}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_catalog(path: Path = CATALOG) -> dict:
    data = json.loads(path.read_text())
    if data.get("schema_version") != 2 or "blocks" in data:
        raise ValueError("Expected a version 2 catalog index")
    files = data["block_files"]
    if len(files) != len(set(files)):
        raise ValueError("Duplicate chapter catalog paths")
    if any(not re.fullmatch(r"chapters/(?:ch\d{2}|intro|part\d+)\.json", name) for name in files):
        raise ValueError("Invalid chapter catalog path")
    actual = {p.relative_to(path.parent).as_posix() for p in (path.parent / "chapters").glob("*.json")}
    if set(files) != actual:
        raise ValueError("Chapter catalog file set mismatch")
    blocks = []
    for name in files:
        chapter = Path(name).stem
        rows = json.loads((path.parent / name).read_text())
        if not isinstance(rows, list) or not rows:
            raise ValueError(f"Empty or invalid chapter catalog: {name}")
        if any(row["source"] != f"books/lean4-formalization/{chapter}.md" for row in rows):
            raise ValueError(f"Block assigned to the wrong chapter: {name}")
        blocks.extend(rows)
    data["blocks"] = blocks
    return data


def extract(book: Path = BOOK) -> list[dict]:
    blocks = []
    for path in sorted(book.glob("*.md")):
        lines = path.read_text().splitlines(keepends=True)
        start = None
        fence = ""
        language = ""
        number = 0
        headings: list[str] = []
        for index, line in enumerate(lines):
            if start is None:
                match = re.match(r"^ {0,3}(`{3,}|~{3,})([^\n]*)\n?$", line)
                if match:
                    fence, language = match.groups()
                    language = language.strip().split(":", 1)[0]
                    start = index
                elif re.match(r"^#{1,6} ", line):
                    level = len(line) - len(line.lstrip("#"))
                    headings = headings[:level - 1] + [line.strip()]
            elif re.match(r"^ {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$", line):
                if language == "lean":
                    number += 1
                    code = "".join(lines[start + 1:index])
                    blocks.append({
                        "id": f"{path.stem}_{number:03}",
                        "source": path.relative_to(REPO).as_posix(),
                        "line": start + 1,
                        "end": index + 1,
                        "sha256": digest(code),
                        "code": code,
                        "section": " / ".join(headings),
                    })
                start = None
        if start is not None:
            raise ValueError(f"Unclosed fence: {path.name}:{start + 1}")
    return blocks


def validate(data: dict | None = None) -> tuple[dict, dict]:
    if data is None:
        data = load_catalog()
    actual = {block["id"]: block for block in extract()}
    rows = data["blocks"]
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate block IDs in catalog")
    if set(ids) != set(actual):
        raise ValueError(f"Inventory coverage mismatch: {set(ids) ^ set(actual)}")
    files = {path.relative_to(REPO).as_posix(): digest(path.read_text())
             for path in BOOK.glob("*.md")}
    if files != data["source_files"]:
        raise ValueError("Manuscript file set or content changed; review and update the catalog")
    for row in rows:
        block = actual[row["id"]]
        for key in ("source", "line", "end", "sha256"):
            if row[key] != block[key]:
                raise ValueError(f"{row['id']}: stale {key}; inspect the source before updating")
        if row["category"] not in LABELS:
            raise ValueError(f"{row['id']}: unknown category")
        if not row["reason"] or not row["context"]["instruction"]:
            raise ValueError(f"{row['id']}: missing classification/context explanation")
        if not set(row["context"]["blocks"]) <= set(actual):
            raise ValueError(f"{row['id']}: dangling context reference")
        if row["category"] == "fragment" and not row["context"]["blocks"]:
            raise ValueError(f"{row['id']}: fragment has no insertion context")
        expected_fixture = f".generated/raw/{row['id']}.lean"
        if row["fixture"] != expected_fixture:
            raise ValueError(f"{row['id']}: invalid fixture path")
        chapter = Path(row["source"]).stem
        if chapter.startswith("ch") and row["repair_stage"] != (2 if int(chapter[2:]) <= 5 else 3 if int(chapter[2:]) <= 11 else 4):
            raise ValueError(f"{row['id']}: unexpected chapter repair stage")
    for mapping in data["compiled_mappings"]:
        code = actual[mapping["block"]]["code"]
        target = ROOT / mapping["module_file"]
        text = target.read_text()
        marker = mapping["block"]
        start = f"-- BEGIN SOURCE {marker}\n"
        end = f"-- END SOURCE {marker}"
        if text.count(start) != 1 or text.count(end) != 1:
            raise ValueError(f"Missing source markers: {target}")
        body = text.split(start, 1)[1].split(end, 1)[0]
        expected = "".join(line for line in code.splitlines(keepends=True)
                           if not line.startswith("import "))
        if body != expected:
            raise ValueError(f"Compiled example differs from source: {marker}")
        for line in code.splitlines():
            if line.startswith("import ") and line not in text.splitlines():
                raise ValueError(f"Missing original import: {marker}: {line}")
    issues = json.loads((ROOT / "catalog/issues.json").read_text())
    if len({item["id"] for item in issues}) != len(issues):
        raise ValueError("Duplicate issue IDs")
    if {f"P1-{i:02}" for i in range(1, 9)} - {item["id"] for item in issues}:
        raise ValueError("Missing priority-one issue")
    for item in issues:
        if not set(item["blocks"]) <= set(actual):
            raise ValueError(f"{item['id']}: dangling issue block reference")
        if item["stage"] not in range(1, 7) or not item["acceptance"]:
            raise ValueError(f"{item['id']}: missing stage or completion criterion")
        for location in item["locations"]:
            if location["source"] not in data["source_files"]:
                raise ValueError(f"{item['id']}: unknown manuscript source")
            if location["line"] < 1 or location["end"] < location["line"]:
                raise ValueError(f"{item['id']}: invalid line range")
    for row in rows:
        expected_issues = [item["id"] for item in issues if row["id"] in item["blocks"]]
        if row["issue_ids"] != expected_issues:
            raise ValueError(f"{row['id']}: inconsistent issue links")
        if row["priority_one"] != any(identity.startswith("P1-") for identity in expected_issues):
            raise ValueError(f"{row['id']}: inconsistent priority flag")
    return data, actual


def render(data: dict) -> str:
    counts = Counter(row["category"] for row in data["blocks"])
    lines = ["# 原稿コードの分類と検証先", "",
             "この表の分類は掲載目的を表し、実行成功の判定ではありません。完成例に不備があっても完成例のまま修正対象として残します。", "",
             "前回の一次点検は各ブロックに import Mathlib を補って独立実行した結果です。本文の前提を引き継がないため、正常終了もエラーも完成度の判定には使いません。", "",
             "第0段階のビルド対象は [README](../README.md) を参照してください。断片の文脈指定は組立て方の指示で、組立て済み・証明済みを意味しません。", "",
             "生のコードは `python3 scripts/catalog.py extract` で `.generated/raw/ID.lean` に、importも含めて原文どおり抽出されます。", "",
             "| 分類 | 数 |", "|---|---:|"]
    lines += [f"| {label} | {counts[key]} |" for key, label in LABELS.items()]
    lines += ["", "対応表と機械可読データは章ごとに分けています。原稿全体の版とファイル一覧は [index.json](index.json) に記録しています。", "",
              "| 原稿 | ブロック数 | 分類・文脈の表 | 機械可読データ |", "|---|---:|---|---|"]
    for source in sorted(data["source_files"]):
        chapter = Path(source).stem
        count = sum(row["source"] == source for row in data["blocks"])
        table = f"[対応表](chapters/{chapter}.md)" if count else "Leanコードなし"
        raw = f"[JSON](chapters/{chapter}.json)" if count else "—"
        lines.append(f"| [{chapter}.md](../../{source}) | {count} | {table} | {raw} |")
    return "\n".join(lines) + "\n"


def render_chapter(chapter: str, rows: list[dict]) -> str:
    lines = [f"# {chapter} のコード分類と検証先", "", "[全体の分類・検証範囲](../README.md) / " + f"[この章のJSON]({chapter}.json)", "",
             "分類は掲載目的を表します。前回の一次点検や文脈の指定は、この章の全例が証明済みという意味ではありません。", "",
             "| ID / 原稿 | 分類 | 掲載位置 | 前回の一次点検 | 文脈・挿入位置 | 修正段階 |",
              "|---|---|---|---|---|---|---|"]
    for row in rows:
        href = "../../../" + row["source"] + f"#L{row['line']}"
        old = row["prior_probe"]
        result = old["status"] + (" / sorry警告" if old["sorry_warning"] else "")
        context = ", ".join(row["context"]["blocks"])
        detail = (context + "：" if context else "") + row["context"]["instruction"]
        fields = [f"[{row['id']}:{row['line']}]({href})", LABELS[row["category"]], row["role"], result,
                  detail, str(row["repair_stage"]) + ("（P1対応は1で先行）" if row["priority_one"] else "")]
        lines.append("| " + " | ".join(field.replace("|", "\\|").replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines) + "\n"


def render_issues() -> str:
    issues = json.loads((ROOT / "catalog/issues.json").read_text())
    base = json.loads(CATALOG.read_text())["review_base"]
    lines = ["# レビュー指摘と修正段階", "",
             "段階0では対応関係を記録します。以下の指摘は本文への修正をまだ完了していません。位置は初回レビューの版への固定リンクです。再掲や関連説明も各段階で照合します。", "",
             "コードと重ならない文章・画像の指摘にもIDを付けています。ブロック数と指摘数は一致しません。完了条件の全文は issues.json に記録しています。", "",
             "| ID | 段階 | 対象 | 問題と修正方針 | 状態 |", "|---|---:|---|---|---|"]
    for item in issues:
        links = [f"[{Path(p['source']).name}:{p['line']}](https://github.com/sakuramaguro/zenn-articles/blob/{base}/{p['source']}#L{p['line']}-L{p['end']})"
                 for p in item["locations"]]
        where = "、".join(links) if links else item["scope"]
        fields = [item["id"], str(item["stage"]), where, item["description"], item["status"]]
        lines.append("| " + " | ".join(f.replace("|", "\\|").replace("\n", " ") for f in fields) + " |")
    return "\n".join(lines) + "\n"


def documents(data: dict) -> dict[str, str]:
    result = {"README.md": render(data), "ISSUES.md": render_issues()}
    for name in data["block_files"]:
        chapter = Path(name).stem
        rows = [row for row in data["blocks"] if Path(row["source"]).stem == chapter]
        result[f"chapters/{chapter}.md"] = render_chapter(chapter, rows)
    return result


def check_documents(data: dict) -> None:
    expected = documents(data)
    chapter_pages = {p.relative_to(CATALOG.parent).as_posix() for p in (CATALOG.parent / "chapters").glob("*.md")}
    if chapter_pages != {name for name in expected if name.startswith("chapters/")}:
        raise ValueError("Chapter table file set mismatch")
    for name, content in expected.items():
        if (CATALOG.parent / name).read_text() != content:
            raise ValueError(f"Table is stale: {name}; run catalog.py extract")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check", "extract"])
    args = parser.parse_args()
    data, actual = validate()
    if args.action == "extract":
        out = ROOT / ".generated/raw"
        out.mkdir(parents=True, exist_ok=True)
        for block in actual.values():
            (out / f"{block['id']}.lean").write_text(block["code"])
        for name, content in documents(data).items():
            (CATALOG.parent / name).write_text(content)
    check_documents(data)
    print(json.dumps({"files": len(data["source_files"]), "blocks": len(actual),
                      "categories": dict(Counter(row["category"] for row in data["blocks"]))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
