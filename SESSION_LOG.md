# Session log

## 2026-11-11 — web interface and interactive course site (branch `web-interface`)
- Added the web interface (`web/`, `run_web.py`, port 8164) and the static GitHub Pages site
  (`scripts/build_static.py`, `.github/workflows/pages.yml`): 9 lessons in README outline order, each with the README
  outline item, live figures (JS ports of every script's maths, sliders), docstrings and highlighted source.
- JS engines checked against Python: `tests/fixtures/course_fixture.json` (99 cases from `web/compute.py`, incl.
  Python `random` and numpy random streams) replayed by `web/static/engines.test.mjs`; all agree to 1e-9 (stats 1e-8).
  In the local app all 26 "Check with Python" buttons report identical results.
- Bugs fixed in the scripts (separate commits, regression tests in `test_regressions.py`, hyphenated copies kept identical):
  Egyptian multiplication table empty / duplicated steps, Babylonian sqrt(0); Chinese numerals trailing 零 and
  KeyError >= 100000, Babylonian 0; golden-ratio pairs repeated; "Multiple of Fib" always true and n=1 crash;
  IP3R domain results overwritten, PROSITE motifs never matching, mRNA codon check; compare_species switching species;
  unused pandas/requests imports and missing biopython requirement; README code-structure section.
- Open questions for George are listed in the web-interface report (IP3R domain positions in residues vs nucleotides,
  provenance of the tree/shell "real data", hyphenated duplicate scripts).
