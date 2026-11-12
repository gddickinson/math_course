"""The course map for the web interface: which README section and which scripts make up each lesson.

All lesson text comes from the repository itself: the README's course outline (the numbered items under each
module) and the docstrings and source of the Python scripts, read with `ast` (nothing is imported or run here).
"""
import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

# Lessons in course order. readme: list of (README "###" heading, item number or None for the whole section).
LESSONS = [
    {"id": "numerals", "title": "Ancient Number Systems", "module": "Module 1",
     "readme": [("Module 1: Foundations and Number Theory", 1)],
     "scripts": ["ancient_numbers.py", "world_numbers.py"]},
    {"id": "calculations", "title": "Early Computational Methods", "module": "Module 1",
     "readme": [("Module 1: Foundations and Number Theory", 1)],
     "scripts": ["ancient_calculations.py", "ancient_math_visualization.py"]},
    {"id": "number-theory", "title": "Number Theory Foundations", "module": "Module 1",
     "readme": [("Module 1: Foundations and Number Theory", 2)],
     "scripts": ["number_theory_basics.py"]},
    {"id": "bio-number-theory", "title": "Number Theory in Biology", "module": "Module 1",
     "readme": [("Module 1: Foundations and Number Theory", 1), ("Module 1: Foundations and Number Theory", 2)],
     "scripts": ["bio_number_theory.py"]},
    {"id": "patterns", "title": "Fibonacci, Phyllotaxis and the Golden Ratio", "module": "Module 3",
     "readme": [("Module 3: Geometry and Trigonometry", 1)],
     "scripts": ["bio_math_patterns.py", "bio_math_enhanced.py", "math_bio_demo.py"]},
    {"id": "growth", "title": "Growth Patterns and Population Models", "module": "Special Topics",
     "readme": [("Special Topics in Mathematical Biology", 1), ("Special Topics in Mathematical Biology", 3)],
     "scripts": ["bio_growth_patterns.py"]},
    {"id": "trees", "title": "Tree Branching", "module": "Special Topics",
     "readme": [("Special Topics in Mathematical Biology", 1)],
     "scripts": ["advanced_tree_patterns.py", "tree_data_analysis.py"]},
    {"id": "shells", "title": "Shell Growth", "module": "Special Topics",
     "readme": [("Special Topics in Mathematical Biology", 1)],
     "scripts": ["shell_growth_patterns.py", "shell_comparative_analysis.py"]},
    {"id": "sequences", "title": "Biological Sequences", "module": "Special Topics",
     "readme": [("Special Topics in Mathematical Biology", 2)],
     "scripts": ["bio_sequence_analysis.py", "ip3r_analysis.py"]},
]
BY_ID = {lesson["id"]: lesson for lesson in LESSONS}


def readme_text() -> str:
    return README.read_text(encoding="utf-8")


def readme_sections(text: str | None = None) -> dict:
    """Map each '### heading' (and '## heading') of the README to the markdown under it."""
    text = text if text is not None else readme_text()
    out, head, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^#{2,3} (.+)$", line)
        if m:
            if head:
                out[head] = "\n".join(buf).strip()
            head, buf = m.group(1).strip(), []
        elif head:
            buf.append(line)
    if head:
        out[head] = "\n".join(buf).strip()
    return out


def readme_item(section_md: str, number: int) -> tuple[str, str]:
    """The numbered top-level item `number` of a section: (item title, markdown of its sub-list)."""
    items, cur = [], None
    for line in section_md.splitlines():
        m = re.match(r"^(\d+)\. (.+)$", line)
        if m:
            cur = [m.group(2).strip(), []]
            items.append(cur)
        elif cur is not None:
            cur[1].append(line)
    title, body = items[number - 1]
    lines = [ln for ln in body if ln.strip() and ln.strip() != "---"]
    indent = min(len(ln) - len(ln.lstrip()) for ln in lines) if lines else 0
    return title, "\n".join(ln[indent:] for ln in lines)


def lesson_readme(lesson: dict) -> list[dict]:
    secs = readme_sections()
    out = []
    for heading, number in lesson["readme"]:
        title, body = readme_item(secs[heading], number) if number else (heading, secs[heading])
        source = f"README.md: {heading}" + (f", item {number}" if number else "")
        out.append({"source": source, "title": title, "markdown": body})
    return out


def _signature(node: ast.FunctionDef) -> str:
    args = [a.arg for a in node.args.args if a.arg != "self"]
    return f"{node.name}({', '.join(args)})"


def script_docs(path: Path) -> list[dict]:
    """Classes, methods and functions of a script with their docstrings, in source order."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docs = []
    mod = ast.get_docstring(tree)
    if mod:
        docs.append({"kind": "module", "name": path.name, "doc": mod, "line": 1})
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            docs.append({"kind": "class", "name": node.name, "doc": ast.get_docstring(node) or "", "line": node.lineno})
            for sub in node.body:
                if isinstance(sub, ast.FunctionDef) and not sub.name.startswith("__"):
                    docs.append({"kind": "method", "name": f"{node.name}.{_signature(sub)}",
                                 "doc": ast.get_docstring(sub) or "", "line": sub.lineno})
        elif isinstance(node, ast.FunctionDef):
            docs.append({"kind": "function", "name": _signature(node), "doc": ast.get_docstring(node) or "",
                         "line": node.lineno})
    return docs


def script_payload(name: str) -> dict:
    path = ROOT / name
    code = path.read_text(encoding="utf-8")
    imports = sorted({m.split(".")[0] for m in re.findall(r"^(?:from|import) ([\w.]+)", code, re.M)})
    return {"file": name, "lines": code.count("\n") + 1, "imports": imports, "docs": script_docs(path), "code": code}


def lesson_payload(lesson_id: str) -> dict:
    lesson = BY_ID[lesson_id]
    i = LESSONS.index(lesson)
    nav = {"prev": LESSONS[i - 1]["id"] if i else None, "next": LESSONS[i + 1]["id"] if i + 1 < len(LESSONS) else None}
    return {**{k: lesson[k] for k in ("id", "title", "module", "scripts")}, "number": i + 1, **nav,
            "readme": lesson_readme(lesson), "files": [script_payload(s) for s in lesson["scripts"]]}


def course_payload() -> dict:
    """Lesson list plus the README outline, marking which README modules have code in the repo."""
    secs = readme_sections()
    covered = {h for lesson in LESSONS for h, _ in lesson["readme"]}
    modules = [{"heading": h, "markdown": secs[h], "has_code": h in covered}
               for h in secs if h.startswith("Module ") or h.startswith("Special Topics")]
    lessons = []
    for i, lesson in enumerate(LESSONS):
        first = lesson["readme"][0]
        items = [readme_item(secs[first[0]], first[1])[0]] if first[1] else []
        lessons.append({"id": lesson["id"], "number": i + 1, "title": lesson["title"], "module": lesson["module"],
                        "scripts": lesson["scripts"], "readme_items": items})
    return {"lessons": lessons, "modules": modules,
            "intro": secs.get("Course Philosophy", ""), "prerequisites": secs.get("Prerequisites", ""),
            "outcomes": secs.get("Learning Outcomes", "")}
