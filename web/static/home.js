// Home page: hero, counts from /api/info, one card per lesson (from /api/course), how the site works.
import { route, api, app, esc, list, tags, isStatic } from './core.js';
import { markdown } from './md.js';

route('home', async () => {
  const [info, course] = await Promise.all([api('/info'), api('/course')]);
  app().innerHTML = `
  <section class="hero">
    <p class="kicker">Math course for biologists · examples in Python</p>
    <h1 class="glow">Advanced Mathematics and Mathematical Biology</h1>
    <p class="lead">Historical mathematics and its biological applications, one lesson per group of the course's
    Python scripts: read the course outline, play with every example as a live figure, then read and run the code.</p>
    <a class="btn" href="#/lesson/${course.lessons[0].id}">Start lesson 1</a><a class="btn alt" href="#/syllabus">Course outline</a>
  </section>
  <div class="tiles">
    <div class="tile"><b>${info.lessons}</b><span>lessons</span></div>
    <div class="tile"><b>${info.scripts}</b><span>Python scripts shown in full</span></div>
    <div class="tile"><b>${info.functions}</b><span>script functions ported to live figures</span></div>
    <div class="tile"><b>${info.fixture_checks}</b><span>Python results the browser code must match</span></div>
    <div class="tile"><b>${info.modules_with_code}/${info.modules_outlined}</b><span>outline sections with code so far</span></div>
  </div>
  <h2>Course philosophy</h2>
  <div class="panel">${markdown(course.intro)}<p class="src small">README.md: Course Philosophy</p></div>
  <h2>Lessons</h2>
  <div class="grid wide lessons">${list(course.lessons, l => `
    <a class="card" href="#/lesson/${esc(l.id)}">
      <small>Lesson ${l.number} · ${esc(l.module)}</small><b>${esc(l.title)}</b>
      <div>${tags(l.scripts, 'c')}</div>
    </a>`)}</div>
  <h2>How this site works</h2>
  <div class="flow">
    <div>The lesson text is the README's course outline and the scripts' own docstrings, read straight from the repository.</div>
    <div>Each script's maths (number systems, Euclid, sieves, Fibonacci, growth models, statistics, sequence counts) is
      ported to a small JavaScript module, so every figure has live sliders.</div>
    <div>Node tests replay ${info.fixture_checks} results of the Python code (including its random numbers) and require the
      JavaScript to agree to 1e-9.</div>
    <div>${isStatic() ? 'Run the app locally (see About) to' : 'In this local app you can'} press "Check with Python" on any
      figure to re-run it through the real scripts.</div>
  </div>`;
});
