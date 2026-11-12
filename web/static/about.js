// About: what the course and this site are, how to run the scripts, the web app and the static build, credits.
import { route, app, isStatic } from './core.js';

route('about', () => {
  app().innerHTML = `
  <section class="hero"><p class="kicker">About</p><h1 class="glow">Math Course for Biologists</h1>
  <p class="lead">"Math course for biologists with examples using python": standalone Python scripts on ancient number
  systems, number theory, Fibonacci patterns, growth models, tree and shell geometry and sequence analysis, by George
  Dickinson. This site turns them into an interactive course.</p></section>
  <h2>What is on this site</h2>
  <ul>
    <li><b>Lessons</b>: one page per group of scripts, in the order of the README's course outline: the outline text,
      live figures, the scripts' docstrings and their full source code.</li>
    <li><b>Live figures</b>: the maths of each script ported to JavaScript and tested against the Python results
      (<code>web/static/*_engine.js</code>, <code>tests/fixtures/course_fixture.json</code>).</li>
    <li><b>Data</b>: the tree, shell and species tables are the values written in the scripts' classes
      (<code>EXAMPLE_TREE_DATA</code>, <code>SHELL_DATA</code>, <code>SPECIES_PARAMETERS</code>, ...): illustrative example
      values written for the course, not measurements; the course does not include measured datasets. Sequences are
      pasted by you (or random).</li>
    <li>${isStatic() ? 'This static copy needs no server.' : 'This local app'} also ${isStatic() ? 'has a local version that can' : 'can'}
      re-run any figure through the real Python code ("Check with Python").</li>
  </ul>
  <h2>Run the scripts</h2>
  <pre>git clone https://github.com/gddickinson/math_course.git
cd math_course
pip install -r requirements.txt
python ancient_numbers.py            # or any other script
python -m pytest test_math_course.py test_regressions.py</pre>
  <p class="small">The NCBI scripts (<code>bio_sequence_analysis.py</code>, <code>ip3r_analysis.py</code>,
  <code>math_bio_demo.py</code> example 2) need biopython and an internet connection; put your own e-mail address in
  them (NCBI asks for one). <code>ancient_math_visualization.py</code> is a Tkinter app.</p>
  <h2>Run the web app</h2>
  <pre>pip install -r requirements-web.txt
python run_web.py                    # http://127.0.0.1:8164
python scripts/build_static.py       # static copy in site/ (as published on GitHub Pages)</pre>
  <h2>Credits</h2>
  <p>Course and scripts by George Dickinson (<a href="https://github.com/gddickinson/math_course" target="_blank" rel="noopener">gddickinson/math_course</a>, MIT licence).
  Built with AI assistance from <a href="https://claude.com/" target="_blank" rel="noopener">Claude (Anthropic)</a>, as the README says.</p>`;
});
