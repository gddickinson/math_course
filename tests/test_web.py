"""Web interface tests: every exported endpoint answers, the static build is complete, and the JS engine tests pass.

Run: python -m pytest -q tests/test_web.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from web.app import STATIC, STATIC_ENDPOINTS, app  # noqa: E402

client = TestClient(app)


def test_index_served():
    r = client.get("/")
    assert r.status_code == 200 and "static/main.js" in r.text


@pytest.mark.parametrize("path", STATIC_ENDPOINTS)
def test_endpoint(path):
    r = client.get("/api" + path)
    assert r.status_code == 200, r.text
    assert r.json() is not None


def test_static_build(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_static
    build_static.build(tmp_path / "site")
    assert (tmp_path / "site" / "index.html").read_text().count("APP_STATIC") == 1
    for path in STATIC_ENDPOINTS:
        assert (tmp_path / "site" / "api" / (path.strip("/") + ".json")).exists()


def test_static_assets_referenced_exist():
    html = (STATIC / "index.html").read_text()
    for name in ("style.css", "main.js"):
        assert f"static/{name}" in html and (STATIC / name).exists()


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_js_engine():
    tests = sorted(STATIC.glob("*.test.mjs"))
    for t in tests:
        r = subprocess.run(["node", str(t)], capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr


# --- project-specific -----------------------------------------------------------------------------------------------
import json  # noqa: E402

import numpy as np  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "course_fixture.json"


def _close(a, b):
    """Recursive comparison with a float tolerance (libm differs in the last digit between macOS and Linux)."""
    if isinstance(a, dict):
        return isinstance(b, dict) and a.keys() == b.keys() and all(_close(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return isinstance(b, list) and len(a) == len(b) and all(_close(x, y) for x, y in zip(a, b))
    if isinstance(a, float) or isinstance(b, float):
        return bool(np.isclose(a, b, rtol=1e-9, atol=1e-12))
    return a == b


def test_fixture_is_current():
    sys.path.insert(0, str(ROOT / "scripts"))
    import make_course_fixture
    fresh = json.loads(json.dumps(make_course_fixture.build()))
    assert _close(fresh, json.loads(FIXTURE.read_text())), "run python scripts/make_course_fixture.py"


def test_every_script_is_in_a_lesson():
    from web.course import LESSONS
    shown = {s for lesson in LESSONS for s in lesson["scripts"]}
    scripts = {p.name for p in ROOT.glob("*.py") if "-" not in p.name and not p.name.startswith(("test_", "run_web"))}
    assert scripts == shown


def test_lessons_have_readme_text_and_code():
    for lesson in client.get("/api/course").json()["lessons"]:
        p = client.get(f"/api/lesson/{lesson['id']}").json()
        assert p["readme"] and all(r["markdown"].startswith("- ") for r in p["readme"])
        assert all(f["code"] and f["docs"] for f in p["files"])


def test_unknown_lesson_404():
    assert client.get("/api/lesson/nope").status_code == 404


@pytest.mark.parametrize("name", ["numerals", "gcd", "advanced_tree", "tree_compare", "sequence"])
def test_python_endpoint_matches_fixture(name):
    case = json.loads(FIXTURE.read_text())["cases"][name][0]
    r = client.post(f"/api/python/{name}", json=case["params"])
    assert r.status_code == 200, r.text
    assert _close(json.loads(json.dumps(r.json()["result"])), case["result"])


def test_python_endpoint_rejects_bad_input():
    assert client.post("/api/python/nope", json={}).status_code == 404
    assert client.post("/api/python/primes", json={"limit": 10**9}).status_code == 400
    assert client.post("/api/python/numerals", json={}).status_code == 400
    assert client.post("/api/python/sequence", json={"seq": "A" * 200001}).status_code == 400


def test_data_tables_come_from_the_scripts():
    from shell_comparative_analysis import ShellComparativeAnalysis
    from tree_data_analysis import TreeDataAnalysis
    d = client.get("/api/data").json()
    assert d["tree_data"] == TreeDataAnalysis.EXAMPLE_TREE_DATA
    assert d["shell_data"].keys() == ShellComparativeAnalysis.SHELL_DATA.keys()
