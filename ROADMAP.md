# Advanced Mathematics and Mathematical Biology Course — Roadmap

## Current State
A collection of 16+ standalone Python scripts implementing mathematical concepts with biological applications. Covers ancient number systems, number theory, bio-math patterns, growth models, shell analysis, tree patterns, and IP3R analysis. Scripts are flat files in the project root with no package structure, no shared utilities, and no module organization matching the ambitious 7-module course outline in the README. The README describes a full course but the implementation covers only portions of Modules 1 and the Special Topics.

## Short-term Improvements
- [ ] Organize scripts into directories matching the README's module structure (`module1/`, `module2/`, etc.)
- [ ] Extract shared utilities (plotting helpers, number conversion functions) from individual scripts into a `utils/` module
- [x] Add `requirements.txt` — scripts likely need `numpy`, `matplotlib`, `scipy`, `sympy`
- [ ] Add `__init__.py` files to make modules importable
- [x] Remove `.ipynb_checkpoints/` directory from version control (add to `.gitignore`)
- [ ] Add consistent docstrings and section headers to all scripts
- [x] Rename files to remove hyphens (use underscores): `ancient-numbers.py` -> `ancient_numbers.py` (hyphens prevent Python imports)

## Feature Enhancements
- [ ] Implement missing Module 2 content: algebraic systems, enzyme kinetics, population modeling
- [ ] Implement missing Module 3 content: computational geometry, phyllotaxis, trigonometry
- [ ] Implement missing Module 4 content: numerical differentiation/integration, growth rate modeling
- [ ] Add Jupyter notebooks alongside scripts for interactive exploration
- [ ] Add exercises/problem sets as separate files with solution keys
- [ ] Add interactive visualizations using `plotly` or `ipywidgets` instead of static matplotlib
- [ ] Add `ip3r_analysis.py` integration with biological datasets (currently appears standalone)

## Long-term Vision
- [ ] Build as a Jupyter Book or Sphinx-based course website
- [ ] Add auto-grading for exercises using `nbgrader`
- [ ] Create a `pyproject.toml`-based package: `pip install math-bio-course`
- [ ] Add real biological datasets (cicada data, DNA sequences, growth measurements) in a `data/` directory
- [ ] Integrate with biological databases (UniProt, NCBI) for live data examples
- [ ] Add assessment system: quizzes, coding challenges, project templates

## Technical Debt
- [x] Hyphenated filenames (`bio-math-patterns.py`) cannot be imported as Python modules
- [ ] No shared code between scripts — significant duplication of plotting, formatting, and math functions
- [ ] README describes 7 modules but only ~2 are partially implemented
- [ ] `bio_math_enhanced.py` vs `bio-math-patterns.py` — naming inconsistency and potential overlap
- [x] No tests — mathematical functions should have unit tests with known analytical results
- [x] `.ipynb_checkpoints/` is tracked in the repo (now in .gitignore)
- [ ] Scripts lack `if __name__ == "__main__":` guards, making them hard to import safely
