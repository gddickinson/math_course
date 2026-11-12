// Course outline (#/syllabus): the README's seven modules and special topics, marking which have scripts (and
// lessons on this site) so far, plus prerequisites and learning outcomes.
import { route, api, app, esc } from './core.js';
import { markdown } from './md.js';

route('syllabus', async () => {
  const c = await api('/course');
  const byHeading = {};
  for (const l of c.lessons) {
    const lesson = await api(`/lesson/${l.id}`);
    for (const r of lesson.readme) (byHeading[r.source.split(': ')[1].split(', item')[0]] ||= new Set()).add(l);
  }
  app().innerHTML = `
  <section class="hero"><p class="kicker">README.md · Course Structure</p><h1 class="glow">Course outline</h1>
  <p class="lead">The full plan from the README. Sections marked "has code" have Python scripts in the repository and
  lessons on this site; the others are outlined in the README but not implemented yet (see ROADMAP.md).</p></section>
  ${c.modules.map(m => `<div class="panel module ${m.has_code ? 'has' : 'todo'}">
    <h2>${esc(m.heading)} <span class="tag ${m.has_code ? 'a' : ''}">${m.has_code ? 'has code' : 'outline only'}</span></h2>
    ${markdown(m.markdown)}
    ${byHeading[m.heading] ? `<p class="small">Lessons: ${[...byHeading[m.heading]].map(l => `<a href="#/lesson/${l.id}">${l.number} · ${esc(l.title)}</a>`).join(' · ')}</p>` : ''}
  </div>`).join('')}
  <div class="two"><div class="panel"><h3>Prerequisites</h3>${markdown(c.prerequisites)}</div>
  <div class="panel"><h3>Learning outcomes</h3>${markdown(c.outcomes)}</div></div>`;
});
