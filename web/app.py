"""FastAPI web app for the Math Course for Biologists: serves the front end in static/ and the JSON API under /api.

Run with `python run_web.py` (http://127.0.0.1:8164, local only). `scripts/build_static.py` exports every path in
STATIC_ENDPOINTS to JSON for the GitHub Pages site, so keep that list in step with the GET routes below.
POST /api/python/<name> runs the course scripts' own code (web/compute.py) for the "Check with Python" buttons;
it exists only in the local app.
"""
from pathlib import Path

from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from web import compute
from web.course import LESSONS, course_payload, lesson_payload, readme_text

STATIC = Path(__file__).resolve().parent / "static"
FIXTURE = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "course_fixture.json"

app = FastAPI(title="Math Course for Biologists")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/info")
def info():
    """Counts for the home page."""
    import json
    scripts = sorted({s for lesson in LESSONS for s in lesson["scripts"]})
    checks = sum(len(v) for v in json.loads(FIXTURE.read_text())["cases"].values()) if FIXTURE.exists() else 0
    return {"title": "Math Course for Biologists", "lessons": len(LESSONS), "scripts": len(scripts),
            "functions": len(compute.REGISTRY), "fixture_checks": checks,
            "modules_with_code": sum(m["has_code"] for m in course_payload()["modules"]),
            "modules_outlined": len(course_payload()["modules"])}


@app.get("/api/course")
def course():
    """Lesson list and the README course outline."""
    return course_payload()


@app.get("/api/readme")
def readme():
    return {"markdown": readme_text()}


@app.get("/api/lesson/{lesson_id}")
def lesson(lesson_id: str):
    """README excerpt, docstrings and source of the scripts for one lesson."""
    try:
        return lesson_payload(lesson_id)
    except KeyError:
        raise HTTPException(404, f"no lesson {lesson_id!r}")


@app.get("/api/data")
def data():
    """Parameter tables and measurement data held in the scripts' class attributes."""
    return compute.data_tables()


LIMITS = {"n": 10**7, "a": 10**9, "b": 10**9, "c": 10**9, "limit": 200000, "length": 200000, "years": 10000,
          "time_steps": 2000, "n_points": 5000, "depth": 12, "iterations": 100}


@app.post("/api/python/{name}")
def python(name: str, params: dict = Body(...)):
    """Run the repo's Python code for one figure (same parameters as the JS engine)."""
    if name not in compute.REGISTRY:
        raise HTTPException(404, f"no function {name!r}")
    for k, lim in LIMITS.items():
        v = params.get(k)
        if isinstance(v, (int, float)) and abs(v) > lim:
            raise HTTPException(400, f"{k} must be at most {lim}")
    if len(str(params.get("seq", ""))) > 200000:
        raise HTTPException(400, "sequence too long (200000 letters max)")
    try:
        return {"name": name, "result": compute.run(name, params)}
    except (KeyError, ValueError, TypeError, ZeroDivisionError, RecursionError) as e:
        raise HTTPException(400, f"{type(e).__name__}: {e}")


# GET paths (without the /api prefix) written to the static site as api/<path>.json.
STATIC_ENDPOINTS = ["/info", "/course", "/readme", "/data"] + [f"/lesson/{lesson['id']}" for lesson in LESSONS]
