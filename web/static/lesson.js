// Lesson page (#/lesson/<id>): the README outline item, the interactive figures for the lesson's scripts, what the
// scripts' docstrings say, and the full Python source (highlighted) with a "run it locally" note.
import { route, api, app, esc, isStatic } from './core.js';
import { markdown } from './md.js';
import { codeBlock } from './highlight.js';

const REPO = 'https://github.com/gddickinson/math_course/blob/main/';
// one module of interactive figures per lesson
const WIDGETS = {
  numerals: () => import('./w_numerals.js'), calculations: () => import('./w_calc.js'),
  'number-theory': () => import('./w_numtheory.js'), 'bio-number-theory': () => import('./w_bionum.js'),
  patterns: () => import('./w_patterns.js'), growth: () => import('./w_growth.js'), trees: () => import('./w_trees.js'),
  shells: () => import('./w_shells.js'), sequences: () => import('./w_sequences.js'),
};
// How each script runs on its own (from the scripts' imports and __main__ blocks).
const RUN_NOTES = {
  'ancient_math_visualization.py': 'opens a Tkinter window with entry boxes for both algorithms.',
  'bio_sequence_analysis.py': 'downloads the human ITPR1 mRNA from NCBI (internet and biopython needed); put your own e-mail in the script first.',
  'ip3r_analysis.py': 'downloads ITPR1 sequences for five species from NCBI (internet and biopython needed); put your own e-mail in the script first.',
  'math_bio_demo.py': 'example 1 runs offline; example 2 downloads the IP3R sequence from NCBI (internet and biopython needed).',
  'bio_math_enhanced.py': 'is a library module (no demo of its own): math_bio_demo.py imports it.',
};

function docsList(docs) {
  const items = docs.filter(d => d.doc || d.kind === 'class');
  if (!items.length) return '<p class="mute small">No docstrings in this file.</p>';
  return `<dl class="docs">${items.map(d => `<div class="doc-${d.kind}"><dt><code>${esc(d.name)}</code>
    <span class="tag">${d.kind}</span></dt><dd>${d.doc ? esc(d.doc).replace(/\n\s*\n/g, '<br><br>') : '<span class="mute">(no docstring)</span>'}</dd></div>`).join('')}</dl>`;
}

function fileBlock(f, open) {
  const note = RUN_NOTES[f.file] || (f.imports.includes('matplotlib')
    ? 'runs the demonstration in its <code>__main__</code> block, printing results and opening matplotlib windows.'
    : 'prints the examples in its <code>__main__</code> block.');
  return `<details class="file" ${open ? 'open' : ''}><summary><code>${esc(f.file)}</code> <span class="mute small">${f.lines} lines ·
    imports ${esc(f.imports.join(', ') || 'nothing')}</span></summary>
    <p class="runnote small">Run it locally: <code>pip install -r requirements.txt</code> then <code>python ${esc(f.file)}</code>: ${note}
    <a href="${REPO}${esc(f.file)}" target="_blank" rel="noopener">View on GitHub</a></p>
    ${codeBlock(f.code)}</details>`;
}

route('lesson', async ([id]) => {
  const [L, data, course] = await Promise.all([api(`/lesson/${id}`), api('/data'), api('/course')]);
  const title = n => course.lessons.find(l => l.id === n)?.title || n;
  const nav = `<nav class="pager" aria-label="Lessons">${L.prev ? `<a class="btn alt" href="#/lesson/${L.prev}">← ${esc(title(L.prev))}</a>` : '<span></span>'}
    ${L.next ? `<a class="btn alt" href="#/lesson/${L.next}">${esc(title(L.next))} →</a>` : '<a class="btn alt" href="#/syllabus">Course outline →</a>'}</nav>`;
  app().innerHTML = `
  <section class="hero lesson-hero">
    <p class="kicker">Lesson ${L.number} of ${course.lessons.length} · ${esc(L.module)}</p>
    <h1 class="glow">${esc(L.title)}</h1>
    <p class="lead">Scripts: ${L.scripts.map(s => `<code>${esc(s)}</code>`).join(', ')}</p>
  </section>
  <h2>From the course outline</h2>
  <div class="outline">${L.readme.map(r => `<div class="panel"><h3>${esc(r.title)}</h3>${markdown(r.markdown)}
    <p class="src small">${esc(r.source)}</p></div>`).join('')}</div>
  <h2>Interactive figures</h2>
  <p class="small mute">Computed in your browser by JavaScript ports of the scripts' own functions, which the test suite
  checks against the Python output. ${isStatic() ? 'In the local app (see About) each figure can also be re-run through the real Python code.'
    : 'Press "Check with Python" to re-run a figure through the real Python code.'}</p>
  <div id="figs"></div>
  <h2>What the code says</h2>
  <p class="small mute">Docstrings of the classes and functions, in source order.</p>
  ${L.files.map(f => `<div class="panel"><h3>${esc(f.file)}</h3>${docsList(f.docs)}</div>`).join('')}
  <h2>The Python code</h2>
  ${L.files.map((f, i) => fileBlock(f, i === 0)).join('')}
  ${nav}`;
  const mod = await WIDGETS[id]();
  mod.mount(document.getElementById('figs'), { data });
});
