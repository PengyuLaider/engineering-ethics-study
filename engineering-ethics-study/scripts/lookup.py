import argparse
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import sys
import unicodedata
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

INDEX_NAME = "教材页索引.jsonl"
BANK_NAME = "题库.jsonl"
ASSISTANT_DIR = "工程伦理学学习助手"
REFERENCES = Path(__file__).resolve().parents[1] / "references"


def find_file(given, name, option):
    if given:
        return given
    if name == BANK_NAME:
        return REFERENCES / "question-bank.jsonl"
    course = Path("期末考试") / ASSISTANT_DIR / name
    candidates = [Path(__file__).resolve().parents[2] / name,
                  Path.cwd() / course, Path.cwd() / ASSISTANT_DIR / name,
                  Path.cwd() / name]
    for path in candidates:
        if path.is_file():
            return path
    raise FileNotFoundError(f"全文检索需要用 {option} 指定 {name}，也可以用 --word 指定带书签的 Word。")


def read_jsonl(path):
    with path.open(encoding="utf-8-sig") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def read_word(path):
    ns = {"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    name = "{" + ns["w"] + "}"
    try:
        with ZipFile(path) as book:
            root = ElementTree.fromstring(book.read("word/document.xml"))
    except (BadZipFile, KeyError, ElementTree.ParseError) as error:
        raise ValueError("请指定可读取的 DOCX 文件。") from error
    body = root.find("w:body", ns)
    if body is None:
        raise ValueError("Word 文件缺少正文。")
    pages = []
    chapter = "正文"
    roman = {5:"I", 6:"II", 10:"I", 11:"II", 12:"III"}
    for node in body:
        bookmark = node.find("w:bookmarkStart", ns)
        if bookmark is not None and (m := re.fullmatch(r"PDF_(\d{3})", bookmark.get(name+"name", ""))):
            n = int(m[1])
            label = "卷首" if n < 10 else "目录" if n < 13 else "参考文献" if 262 <= n <= 265 else "卷末" if n > 265 else chapter
            pages.append({
                "pdf_page":n, "printed_page":n-12 if 13 <= n <= 265 else roman.get(n),
                "word_bookmark":f"PDF_{n:03d}", "chapter":label, "text":[],
            })
        if not pages:
            continue
        paragraphs = [node] if node.tag == name+"p" else node.findall(".//w:p", ns)
        for p in paragraphs:
            style = p.find("w:pPr/w:pStyle", ns)
            role = style.get(name+"val") if style is not None else ""
            if role == "BookLocator":
                continue
            value = "".join(t.text or "" for t in p.findall(".//w:t", ns)).strip(" \r\n\u200b")
            if value:
                pages[-1]["text"].append(value)
                if role == "Heading1":
                    chapter = value
                    pages[-1]["chapter"] = chapter
    if [p["pdf_page"] for p in pages] != list(range(1, 268)):
        raise ValueError("此检索适用于含有 PDF_001 至 PDF_267 页级书签的原书排版版 Word。")
    return pages


def parse_range(spec, maximum):
    values = spec.split("-")
    if len(values) not in (1, 2) or not all(re.fullmatch(r"[0-9]+", value) for value in values):
        raise ValueError("页码使用单个数字或起讫数字，例如 93-95。")
    start, stop = int(values[0]), int(values[-1])
    if not 1 <= start <= stop <= maximum:
        raise ValueError(f"页码应在 1 至 {maximum} 内，且起页不大于终页。")
    return range(start, stop + 1)


def key(text):
    text = unicodedata.normalize("NFKC", text).lower().replace("—", "-").replace("–", "-")
    return re.sub(r"\s+", "", text)


def search(pages, queries, include_front, limit):
    normalized = list(dict.fromkeys(key(q) for q in queries if key(q)))
    if not normalized:
        raise ValueError("请输入至少一个可搜索的词。")
    results = []
    for page in pages:
        if not include_front and not 13 <= page["pdf_page"] <= 265:
            continue
        hits = {}
        counts = 0
        for i, paragraph in enumerate(page["text"], 1):
            content = key(paragraph)
            for term in normalized:
                loc = content.find(term)
                if loc < 0:
                    continue
                counts += min(content.count(term), 4)
                in_body = len(content) >= 35
                if term in hits and (hits[term]["body"] or not in_body):
                    continue
                excerpt = content[max(0, loc-43):loc+len(term)+55]
                hits[term] = {"term": term, "block": i, "excerpt": excerpt, "body": in_body}
        if hits:
            results.append(((len(hits), counts), page, list(hits.values())))
    return sorted(results, key=lambda entry: (-entry[0][0], -entry[0][1], entry[1]["pdf_page"]))[:limit]


def description(page, pdf_mode=False):
    printed = page["printed_page"]
    folio = f"原书第 {printed} 页" if printed else f"文件第 {page['pdf_page']} 页"
    place = f"PDF 第 {page['pdf_page']} 页" if pdf_mode else f"Word 书签 {page['word_bookmark']}"
    return f"{folio} · {place} · {page['chapter']}"


def stem_key(text):
    text = unicodedata.normalize("NFKC", text).strip()
    text = re.sub(r"^(?:第\s*[0-9一二三四五六七八九十]+\s*题\s*[.:、]?|"
                  r"\(?[0-9]{1,3}\s*[.)、](?![0-9]))\s*", "", text)
    han = r"[\u3400-\u9fff]"
    text = re.sub(rf"(?<={han})\s+|\s+(?={han})", "", text)
    return " ".join(text.rstrip(".。!? ").split())


def show_record(record):
    print(f"{record['id']}　{record['type']}")
    print(record["stem"])
    print(record["source"])
    if record.get("options"):
        print("\n".join(record["options"]))
        print("核对来题选项内容与顺序后使用此题库答案。")
    if record.get("official_answer") is not None:
        print(f"已收录的课程答案　{record['official_answer']}")
    if record.get("proposed_answer"):
        print(f"按教材拟答　{record['proposed_answer']}")
    if record.get("points") is not None:
        print(f"自测评分　{record['points']} 分")
    if record.get("grading_rule"):
        print(record["grading_rule"] + "。")
    for row in record.get("rubric") or []:
        pages = "、".join(str(n) for n in row.get("printed_pages", []))
        citation = f"（原书第 {pages} 页）" if pages else ""
        print(f"  {row['p']} 分　{row['criterion']}{citation}")
    if record.get("note"):
        print(record["note"])
    if record.get("law_update"):
        update = record["law_update"]
        print(f"法源检索记录　{update['verified_on']}")
        for ref in update["references"]:
            print(f"  {ref['summary']}\n  {ref['title']} {ref['url']}")


def show_review(records, spec):
    match = re.fullmatch(r"([1-8])\.([1-9][0-9]*)", spec)
    if not match:
        raise ValueError("教材章末题用章.题号，例如 1.5。")
    chapter, number = map(int, match.groups())
    matches = []
    for record in records:
        location = record.get("question_location") or {}
        if (location.get("chapter"), location.get("number")) == (chapter, number):
            matches.append(record)
    if not matches:
        raise ValueError(f"教材中无已收录的第 {chapter} 章第 {number} 道章末题。")
    if len(matches) != 1:
        raise ValueError(f"第 {chapter} 章第 {number} 道章末题有重复记录。")
    show_record(matches[0])


def show_item(records, identifier):
    matches = [record for record in records if record["id"] == identifier]
    if len(matches) != 1:
        raise ValueError(f"应有一条题号为 {identifier} 的记录，实际找到 {len(matches)} 条。")
    show_record(matches[0])


def show_stem_matches(records, text, limit):
    query = stem_key(text)
    if not query:
        raise ValueError("请输入题干文字。")
    exact = []
    related = []
    threshold = 0.64
    for record in records:
        stem = stem_key(record["stem"])
        if stem == query:
            exact.append(record)
            continue
        shorter = min(len(stem), len(query))
        if shorter < 7 or 2 * shorter < threshold * (len(stem) + len(query)):
            continue
        score = SequenceMatcher(None, query, stem, autojunk=False).ratio()
        if score >= threshold:
            related.append((score, record))
    if len(exact) == 1:
        print("题干一致")
        show_record(exact[0])
        return
    if exact:
        print("多条记录的题干一致。请按来源和选项核对题目版本。")
        candidates = exact
    elif related:
        print("相近题干。请核对问法、限定词、选项和题目版本。")
        candidates = [record for _, record in sorted(related, key=lambda entry: -entry[0])]
    else:
        print("题库中未找到相符的题干。可用题目中的关键词回查教材。")
        return
    for record in candidates[:limit]:
        print(f"  {record['id']}　{record['stem']}　{record['source']}")
    if len(candidates) > limit:
        print(f"共找到 {len(candidates)} 条，可用 --limit 展开。")


def page_citation(row):
    printed = "、".join(map(str, row["printed_pages"]))
    bookmarks = "、".join(f"PDF_{p:03d}" for p in row["pdf_pages"])
    return f"原书第 {printed} 页（Word 书签 {bookmarks}）"


def show_section(sections, code):
    identifier = key(code)
    row = next((r for r in sections if r["id"] == identifier), None)
    if row is None:
        raise ValueError("请使用教材节编号，例如 3.5 或 7.4。")
    a, b = row["printed_range"]
    print(f"{identifier}　{row['title']}　原书第 {a}–{b} 页")
    for point in row["points"]:
        print(f"  {point['label']}　{point['summary']}（{page_citation(point)}）")
    print(f"本节原创练习 {row['exercise']}")


def lookup_key(text):
    return "".join(c for c in unicodedata.normalize("NFKC", text).casefold() if c.isalnum())


def alias_score(query, aliases):
    terms = {lookup_key(term) for term in aliases}
    if query in terms:
        return 100
    matches = [len(term) for term in terms if len(term) >= 2 and term in query]
    if matches:
        return max(matches) + min(6, len(matches))
    if len(query) >= 2 and any(query in term for term in terms):
        return 2
    return 0


def show_topic(topics, text, limit):
    query = lookup_key(text)
    if len(query) < 2:
        raise ValueError("请提供至少两个字符的知识点或问题。")
    candidates = [(alias_score(query, [r["title"], *r["aliases"]]), r) for r in topics]
    matched = sorted((item for item in candidates if item[0]), key=lambda item: -item[0])
    if not matched:
        print("未命中跨章主题。可用教材关键词按页检索，或按节编号打开知识点。")
        return
    for _, row in matched[:limit]:
        print(f"{row['title']}　关联节 {'、'.join(row['sections'])}")
        for point in row["points"]:
            print(f"  {point['summary']}（{page_citation(point)}）")


def show_case(cases, text, limit):
    identifier = re.sub(r"^案例", "", key(text))
    embedded = re.search(r"案例\s*([1-8])[-.\s]+(\d{1,2}|末)", key(text))
    if embedded:
        identifier = "-".join(embedded.groups())
    matches = [row for row in cases if row["id"] == identifier]
    if not matches:
        query = lookup_key(re.sub(r"^(?:教材)?案例[：:\s]*", "", text))
        if len(query) < 2:
            raise ValueError("请提供案例编号或至少两个字符的题名，例如 6-5、6-末或三鹿。")
        named = [(alias_score(query, [row["title"], *row.get("aliases",[])]), row) for row in cases]
        exact = [row for score, row in named if score == 100]
        matches = exact or [row for score, row in sorted(named, key=lambda item: -item[0]) if score]
        if not matches and len(query) >= 4:
            ranked = [(SequenceMatcher(None, query, lookup_key(row["title"]), autojunk=False).ratio(), row)
                      for row in cases]
            matches = [row for score, row in sorted(ranked, key=lambda item: -item[0]) if score >= .76]
    if not matches:
        print("未检到对应案例。可试案例编号或题名关键词。")
        return
    if len(matches) > 1:
        print("题名匹配多条案例。可按编号展开。")
        for row in matches[:limit]:
            print(f"  {row['id']}　{row['title']}　{page_citation(row)}")
        print("全文关键词检索还可定位这些事件的其他教材论述。")
        return
    row = matches[0]
    location = row["start"]
    print(f"{row['id']}　{row['title']}")
    print(f"教材起点　原书第 {location['printed_page']} 页（Word 书签 PDF_{location['pdf_page']:03d}）"
          f" 第 {location['block']} 段")
    print(f"教材叙述　{row['book_account']}（{page_citation(row)}）")
    prompts = row.get("textbook_questions")
    if prompts:
        print(f"教材设问　{page_citation(prompts)}")
        for i, question in enumerate(prompts["questions"], 1):
            print(f"  {i}. {question}")
    print(f"分析问题　{row['decision']}")
    print(f"利益相关者　{'、'.join(row['stakeholders'])}")
    print(f"论证路径　{row['analysis']}")
    print(f"对应小节　{'、'.join(row['sections'])}")


def show_questions(records, scope, limit):
    number = key(scope)
    if not re.fullmatch(r"[1-8](?:\.[1-7])?", number):
        raise ValueError("用章号或节编号定位原创练习，例如 5 或 5.2。")
    chapter = int(number[0])
    rows = [r for r in records if r.get("origin") == "原创分节练习"
            and (number in r.get("section_codes", []) if "." in number else chapter in r["chapter"])]
    if not rows:
        raise ValueError(f"本版教材未找到对应的分节练习 {number}。")
    for row in rows[:limit]:
        print(f"{row['id']}　{row['type']}　{row['points']} 分")
        print(row["stem"])
        for option in row["options"]:
            print(f"  {option}")
        if row["type"] == "多选":
            print(row["grading_rule"] + "。")
        print()
    if len(rows) > limit:
        print(f"共 {len(rows)} 题，可用 --limit 展开。")


def main():
    parser = argparse.ArgumentParser(description="查找《工程伦理学》第二版教材页和题库记录。")
    sources = parser.add_mutually_exclusive_group()
    sources.add_argument("--index", type=Path, help="以逐页 JSONL 为全文来源")
    sources.add_argument("--word", type=Path, help="直接读取带 PDF_001 等书签的原书排版版 DOCX")
    parser.add_argument("--bank", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--pdf", help="文件顺序页，例如 105-107。")
    mode.add_argument("--printed", help="书上所印的阿拉伯数字页码，例如 93-95。")
    mode.add_argument("--review", help="教材章末题按章.题号定位，例如 1.5。")
    mode.add_argument("--stem", help="按完整题干查找题库记录。")
    mode.add_argument("--item", help="按题库 ID 打开题目、答案和评分点。")
    mode.add_argument("--section", help="查一节的知识点和教材依据，例如 6.7。")
    mode.add_argument("--topic", help="按自然问法查跨章主题和易混概念。")
    mode.add_argument("--case", help="按编号或题名定位案例，例如 5-10、7-末或三门峡。")
    mode.add_argument("--questions", help="列出指定章或节的原创练习题面，例如 4 或 4.3。")
    parser.add_argument("--limit", type=int, default=8, help="检索返回的最多页数或候选题数。")
    parser.add_argument("--include-front", action="store_true", help="关键词检索时包含目录和扉页。")
    parser.add_argument("queries", nargs="*", help="关键词，以空格分隔。")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit 应为正整数。")
    bank_mode = any(value is not None for value in (args.review, args.stem, args.item, args.questions))
    knowledge_mode = any(value is not None for value in (args.section, args.topic, args.case))
    if bool(args.queries) == (bool(args.pdf or args.printed) or bank_mode or knowledge_mode):
        parser.error("输入关键词，或选择一种页码、知识点、案例或题库检索方式。")
    if args.bank and not bank_mode:
        parser.error("--bank 与 --review、--stem、--item 或 --questions 一起使用。")
    if (args.word or args.index) and (bank_mode or knowledge_mode):
        parser.error("--word 和 --index 用于全文关键词或页码检索。")
    try:
        if knowledge_mode:
            records = read_jsonl(REFERENCES / "knowledge.jsonl")
            if args.section is not None:
                show_section([r for r in records if r["kind"] == "section"], args.section)
            elif args.topic is not None:
                show_topic([r for r in records if r["kind"] == "topic"], args.topic, args.limit)
            else:
                show_case([r for r in records if r["kind"] == "case"], args.case, args.limit)
            return
        if bank_mode:
            records = read_jsonl(find_file(args.bank, BANK_NAME, "--bank"))
            if args.review is not None:
                show_review(records, args.review)
            elif args.item is not None:
                show_item(records, args.item)
            elif args.questions is not None:
                show_questions(records, args.questions, args.limit)
            else:
                show_stem_matches(records, args.stem, args.limit)
            return
        pages = read_word(args.word) if args.word else read_jsonl(find_file(args.index, INDEX_NAME, "--index"))
        if args.pdf or args.printed:
            wanted = parse_range(args.pdf, 267) if args.pdf else parse_range(args.printed, 253)
            for page in pages:
                number = page["pdf_page"] if args.pdf else page["printed_page"]
                if isinstance(number, int) and number in wanted:
                    print(description(page, pdf_mode=bool(args.pdf)))
                    for i, text in enumerate(page["text"], 1):
                        print(f"  {i:02d} {text}")
                    print()
            return
        results = search(pages, args.queries, args.include_front, args.limit)
        if not results:
            print("逐页文本未检到相关词。可按知识地图找同义词或定位原页。")
        for _, page, hits in results:
            print(description(page))
            for hit in hits:
                print(f"  段 {hit['block']:02d} [{hit['term']}] {hit['excerpt']}")
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
