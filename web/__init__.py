"""Web interface for the math course (FastAPI app + static GitHub Pages site).

Contents:
    app.py          FastAPI app: /api/info, /api/course, /api/readme, /api/data, /api/lesson/<id>,
                    POST /api/python/<name>; STATIC_ENDPOINTS for the static export
    course.py       lesson map: README outline items + scripts per lesson, docstrings/source via ast
    compute.py      Python reference results for the figures, calling the course scripts' classes
    compute_seq.py  same for the sequence lesson (bio_sequence_analysis.py, ip3r_analysis.py)
    static/         front end (ES modules, no build step); *_engine.js are the JS ports
"""
