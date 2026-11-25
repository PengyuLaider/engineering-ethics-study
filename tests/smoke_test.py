"""Exercise the packaged Skill from outside its repository root."""

from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
LOOKUP = ROOT / "engineering-ethics-study/scripts/lookup.py"
OPEN_BANK = ROOT / "engineering-ethics-study/references/open-book-bank.jsonl"


def lookup(*args):
    return subprocess.run(
        [sys.executable, str(LOOKUP), *args],
        cwd=ROOT / "tests", capture_output=True, encoding="utf-8", check=True,
    ).stdout


class SkillSmokeTests(unittest.TestCase):
    def test_book_section(self):
        result = lookup("--section", "3.5")
        self.assertIn("主动性责任与被动性责任", result)
        self.assertIn("PDF_105", result)

    def test_cross_chapter_topic(self):
        result = lookup("--topic", "实测能运行，项目就应当实施吗")
        self.assertIn("技术可行与社会可接受", result)
        self.assertIn("认同与满意", result)

    def test_cases_preserve_distinct_textbook_perspectives(self):
        result = lookup("--case", "三鹿")
        self.assertIn("5-1　三鹿毒奶粉事件", result)
        self.assertIn("6-3　三鹿庭审记录", result)

    def test_bundled_questions_and_scoring(self):
        questions = lookup("--questions", "6.5")
        self.assertIn("EE-ORIG-06-05", questions)
        self.assertNotIn("按教材拟答", questions)
        answer = lookup("--item", "EE-ORIG-06-05")
        self.assertEqual(answer.count("  1 分"), 6)
        self.assertIn("自测评分　6 分", answer)

    def test_bundled_review_by_number(self):
        self.assertIn("安全可靠", lookup("--review", "1.5"))

    def test_open_book_bank_v2_grounding(self):
        lines = [line for line in OPEN_BANK.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertEqual(len(lines), 68)
        z4 = lookup("--bank", str(OPEN_BANK), "--item", "EE-OPEN-Z4")
        self.assertIn("不以国家规定为限", z4)
        q29 = lookup("--bank", str(OPEN_BANK), "--item", "EE-OPEN-29")
        self.assertIn("工程造福人类是工程发展的终极目标", q29)
        q63 = lookup("--bank", str(OPEN_BANK), "--item", "EE-OPEN-63")
        self.assertIn("工程良心是有用的，但不是万能的", q63)


if __name__ == "__main__":
    unittest.main()
