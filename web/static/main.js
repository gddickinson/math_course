// Entry point: background, lazy page modules, footer mode, router.
import { start, lazy, route, app, isStatic, $ } from './core.js';
import { background } from './bg.js';

const PAGES = { 'home.js': ['home'], 'lesson.js': ['lesson'], 'syllabus.js': ['syllabus'], 'about.js': ['about'] };
lazy(Object.fromEntries(Object.entries(PAGES).flatMap(([file, names]) => names.map(n => [n, () => import('./' + file)]))));

route('notfound', () => { app().innerHTML = '<h1>Not found</h1><p><a href="#/">Back to the start</a></p>'; });

$('#mode').textContent = isStatic()
  ? 'static site: every figure is computed in your browser'
  : 'local app: browser figures + the course scripts at /api/python';
try { background($('#bg')); } catch (e) { console.warn('background:', e); }
start();
