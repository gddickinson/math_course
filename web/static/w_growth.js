// Lesson 6 figures: bio_growth_patterns.py (BioGrowthPatterns): the recursive fractal tree, the logarithmic
// (nautilus) spiral and the exponential / logistic / Allee population models.
import { tree, shellSpiral, population } from './growth_engine.js';
import { chart, ramp, fmt } from './plot.js';
import { figure, sl, checkbox, num, checkButton } from './ui.js';

function treeFig(host, data) {
  const f = figure(host, 'Fractal tree: recursive branching',
    'Each branch ends in two children turned ±θ, each shorter by the decay factor, until the depth runs out: '
    + 'a tree of depth d has 2^d − 1 branches. Colour and width follow the remaining depth, as in visualize_tree().',
    'BioGrowthPatterns.generate_tree(), visualize_tree()');
  const s = { branching_angle: 30, depth: 8, length_decay: 0.7 };
  const show = () => {
    const segs = tree(s);
    f.out.innerHTML = `<p class="small mute">${segs.length} branches</p><div class="plot sq"></div>`;
    chart(f.out.querySelector('.plot'), { w: 520, h: 520, equal: true, alt: 'fractal tree',
      series: [{ type: 'segments', data: segs.map(d => [d[0], d[1], d[2], d[3], ramp(d[4] / s.depth), Math.max(0.6, d[4] / 1.6)]) }] });
  };
  const ctl = [sl(f.ctl, 'Branching angle θ (°)', 0, 90, 1, s.branching_angle, v => { s.branching_angle = v; show(); }),
    sl(f.ctl, 'Depth', 1, 12, 1, s.depth, v => { s.depth = v; show(); }),
    sl(f.ctl, 'Length decay', 0.3, 0.9, 0.01, s.length_decay, v => { s.length_decay = v; show(); })];
  const p = document.createElement('div');
  p.className = 'presets';
  p.innerHTML = '<span class="small mute">Script examples:</span><button class="alt chip" data-p="30,8">Regular (30°, depth 8)</button>'
    + '<button class="alt chip" data-p="45,7">Wide (45°, depth 7)</button>';
  p.addEventListener('click', e => {
    const v = e.target.dataset?.p; if (!v) return;
    const [a, d] = v.split(',').map(Number);
    ctl[0].value = a; ctl[1].value = d; ctl[2].value = 0.7;
    ctl.forEach(c => c.dispatchEvent(new Event('input')));
  });
  f.ctl.appendChild(p);
  checkButton(f, 'tree', () => ({ ...s }), data);
  show();
}

function shellFig(host, data) {
  const f = figure(host, 'Logarithmic spiral (nautilus shell)',
    'r = a·e^(bθ) over three turns (θ from 0 to 6π): every turn multiplies the radius by e^(2πb), so the shape stays the same as it grows.',
    'BioGrowthPatterns.generate_shell_spiral(), visualize_shell()');
  const s = { n_points: 1000, growth_rate: 0.1, tightness: 1.0 };
  const show = () => {
    const { x, y } = shellSpiral(s);
    f.out.innerHTML = `<p class="eq">r = ${s.tightness}·e<sup>${s.growth_rate}θ</sup> · radius × ${num(Math.exp(2 * Math.PI * s.growth_rate), 3)} per turn</p><div class="plot sq"></div>`;
    chart(f.out.querySelector('.plot'), { w: 480, h: 480, equal: true, alt: 'logarithmic spiral',
      series: [{ type: 'line', x, y, color: 'var(--warn)', width: 2.5 }] });
  };
  const ctl = [sl(f.ctl, 'Growth rate b', 0.02, 0.3, 0.01, s.growth_rate, v => { s.growth_rate = v; show(); }),
    sl(f.ctl, 'Tightness a', 0.5, 2, 0.1, s.tightness, v => { s.tightness = v; show(); })];
  const p = document.createElement('div');
  p.className = 'presets';
  p.innerHTML = '<span class="small mute">Script panels:</span>' + [[0.1, 1.0], [0.2, 0.8], [0.15, 1.2], [0.18, 0.9]]
    .map(([b, a]) => `<button class="alt chip" data-p="${b},${a}">b ${b}, a ${a}</button>`).join('');
  p.addEventListener('click', e => {
    const v = e.target.dataset?.p; if (!v) return;
    v.split(',').forEach((x, i) => { ctl[i].value = x; ctl[i].dispatchEvent(new Event('input')); });
  });
  f.ctl.appendChild(p);
  checkButton(f, 'shell_spiral', () => ({ ...s }), data);
  show();
}

function popFig(host, data) {
  const f = figure(host, 'Population growth: exponential, logistic and Allee models',
    'Discrete time steps. Exponential: P ← P(1 + r). Logistic: P ← P + rP(1 − P/K). Allee (as coded): '
    + 'P ← P + rP·((P − A)/K)·(1 − P/K) with threshold A = half the starting population.',
    'BioGrowthPatterns.simulate_population_growth(), visualize_population()');
  const s = { initial_pop: 100, growth_rate: 0.1, carrying_capacity: 1000, time_steps: 100 };
  const on = { exponential: true, logistic: true, allee: true };
  let logY = false;
  const COL = { exponential: 'var(--accent3)', logistic: 'var(--accent)', allee: 'var(--accent2)' };
  const show = () => {
    const t = Array.from({ length: s.time_steps }, (_, i) => i);
    const series = Object.keys(on).filter(m => on[m]).map(m => ({ type: 'line', x: t, y: population({ ...s, model: m }), color: COL[m], label: m }));
    const ends = series.map(se => `${se.label}: ${fmt(se.y[se.y.length - 1])}`).join(' · ');
    f.out.innerHTML = `<p class="small mute">Population at the last step: ${ends || '–'}</p><div class="plot"></div><div class="plot2"></div>`;
    chart(f.out.querySelector('.plot'), { h: 300, title: 'Comparison of growth models', x: { label: 'time step' },
      y: { label: 'population', log: logY }, series: [...series, { type: 'hline', y: s.carrying_capacity, color: 'var(--mute)', label: 'K' }] });
    chart(f.out.querySelector('.plot2'), { h: 260, title: 'Logistic growth with the script\'s three rates', x: { label: 'time step' },
      y: { label: 'population' }, series: [0.05, 0.1, 0.2].map((r, i) => ({ type: 'line', x: t,
        y: population({ ...s, growth_rate: r, model: 'logistic' }), color: ['#7fd4ff', 'var(--accent3)', '#2f5cff'][i], label: `r = ${r}` })) });
  };
  sl(f.ctl, 'Initial population P₀', 1, 900, 1, s.initial_pop, v => { s.initial_pop = v; show(); });
  sl(f.ctl, 'Growth rate r', 0.01, 3, 0.01, s.growth_rate, v => { s.growth_rate = v; show(); });
  sl(f.ctl, 'Carrying capacity K', 100, 5000, 50, s.carrying_capacity, v => { s.carrying_capacity = v; show(); });
  sl(f.ctl, 'Time steps', 10, 300, 1, s.time_steps, v => { s.time_steps = v; show(); });
  for (const m of Object.keys(on)) checkbox(f.ctl, m, true, c => { on[m] = c; show(); });
  checkbox(f.ctl, 'log scale', false, c => { logY = c; show(); });
  checkButton(f, 'population', () => ({ ...s, model: 'logistic' }), data);
  show();
}

export function mount(host, { data }) {
  treeFig(host, data);
  shellFig(host, data);
  popFig(host, data);
}
