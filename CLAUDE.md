# Math Course

Advanced Mathematics and Mathematical Biology course materials.

## Quick Reference
@INTERFACE.md

## Running
- Individual scripts: `python ancient_numbers.py`, `python number_theory_basics.py`, etc.
- Tests: `python -m pytest test_math_course.py test_regressions.py -v`
- Web app: `python run_web.py` (port 8164); web tests: `python -m pytest -q tests/test_web.py`;
  after changing a script's maths, rerun `python scripts/make_course_fixture.py` and update the JS engine.

## Dependencies
See `requirements.txt`: numpy, matplotlib, scipy, sympy, biopython
(biopython only for the NCBI sequence scripts).
