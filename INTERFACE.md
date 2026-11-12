# Math Course -- Interface Map

## Course scripts (repository root)

| File | Purpose | Key Classes |
|------|---------|-------------|
| `ancient_numbers.py` | Egyptian and Babylonian number systems | `EgyptianNumber`, `BabylonianNumber` |
| `ancient_calculations.py` | Egyptian multiplication, Babylonian square root | `EgyptianMultiplication`, `BabylonianSquareRoot` |
| `ancient_math_visualization.py` | Tkinter app for the two ancient algorithms | `AncientMathVisualizer` |
| `world_numbers.py` | Roman, Mayan, Chinese numeral systems | `RomanNumeral`, `MayanNumeral`, `ChineseNumeral` |
| `number_theory_basics.py` | GCD, primes, sieve, factorization, Diophantine | `NumberTheory` |
| `bio_math_patterns.py` | Fibonacci, phyllotaxis, golden ratio in biology | `BioMathPatterns` |
| `bio_math_enhanced.py` | Enhanced Fibonacci analysis and pattern analysis | `FibonacciAnalyzer`, `MathematicalPatternAnalyzer` |
| `bio_growth_patterns.py` | Fractal trees, shell spiral, population models | `TreeNode`, `BioGrowthPatterns` |
| `bio_number_theory.py` | Number theory applied to biology (cicadas, DNA lengths) | `BioNumberTheory` |
| `bio_sequence_analysis.py` | NCBI DNA sequence analysis (biopython, internet) | `NCBISequenceAnalyzer` |
| `shell_growth_patterns.py` | Shell spiral growth models | `ShellParameters`, `ShellGrowthAnalysis` |
| `shell_comparative_analysis.py` | Comparative shell measurements | `ShellMeasurement`, `ShellComparativeAnalysis` |
| `tree_data_analysis.py` | Tree branching data statistics vs model | `TreeDataAnalysis` |
| `advanced_tree_patterns.py` | Tree model with season/light/nutrients | `TreeNode`, `AdvancedTreeModel` |
| `ip3r_analysis.py` | IP3 receptor sequence/domain analysis (NCBI) | `IP3RAnalyzer` |
| `math_bio_demo.py` | Demo combining the pattern analyzers and IP3R | (script) |
| `test_math_course.py` | Unit tests | (tests) |
| `test_regressions.py` | Regression tests for fixed bugs | (tests) |

## Web interface (`web/`, see `web/__init__.py`)

| File | Purpose |
|------|---------|
| `run_web.py` | starts the FastAPI app on 127.0.0.1:8164 |
| `web/app.py` | routes: `/api/info`, `/api/course`, `/api/readme`, `/api/data`, `/api/lesson/<id>`, POST `/api/python/<name>`; `STATIC_ENDPOINTS` |
| `web/course.py` | `LESSONS` (README outline item + scripts per lesson), README parsing, docstrings/source via `ast` |
| `web/compute.py` | `REGISTRY` of Python reference functions calling the scripts' classes; `data_tables()` |
| `web/compute_seq.py` | reference functions for the sequence lesson (`sequence`, `ip3r`) |
| `web/static/core.js`, `style.css` | shared web-kit router/helpers and theme (unchanged copies) |
| `web/static/main.js`, `static_api.js`, `bg.js` | entry point, static-site data layer, background |
| `web/static/home.js`, `syllabus.js`, `about.js`, `lesson.js` | pages; `lesson.js` loads one `w_<lesson>.js` figure module |
| `web/static/w_*.js` | figures per lesson (numerals, calc, numtheory, bionum, patterns, growth, trees, shells, sequences) |
| `web/static/*_engine.js`, `pyrandom.js` | JS ports: numerals, numtheory, patterns, growth, tree, stats, sequence; Python/numpy MT19937 |
| `web/static/js_compute.js` | JS `REGISTRY` with the same names as `web/compute.py`, `diff()` |
| `web/static/plot.js`, `ui.js`, `md.js`, `highlight.js` | SVG charts, controls, tiny markdown renderer, Python highlighter |
| `web/static/engines.test.mjs`, `text.test.mjs` | node tests (fixture replay; markdown/highlighter) |
| `scripts/make_course_fixture.py` | writes `tests/fixtures/course_fixture.json` from `web/compute.py` |
| `scripts/build_static.py`, `scripts/screenshots.py` | static export for GitHub Pages; Playwright smoke test / README images |
| `tests/test_web.py` | API, static build, fixture-current, Python endpoint, node tests |

Flow: `web/compute.py` (Python, real classes) == `js_compute.js` (browser), checked by the fixture and by "Check with
Python" in the local app.

## Notes

- Hyphenated originals (e.g., `ancient-numbers.py`) are identical copies kept for backward compatibility.
  The underscore versions (e.g., `ancient_numbers.py`) are the importable copies; bug fixes were applied to both.
- `bio_math_enhanced.py` vs `bio_math_patterns.py`: enhanced version adds `FibonacciAnalyzer`
  and `MathematicalPatternAnalyzer` with more advanced analysis; patterns has the base `BioMathPatterns`.
