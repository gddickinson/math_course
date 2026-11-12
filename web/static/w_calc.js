// Lesson 2 figures: ancient_calculations.py and ancient_math_visualization.py: Egyptian (doubling) multiplication
// and the Babylonian square-root iteration with its convergence plots.
import { egyptianMultiply, babylonianSqrt } from './numerals_engine.js';
import { chart, fmt } from './plot.js';
import { figure, sl, numInput, table, checkButton } from './ui.js';

function egyptian(host, data) {
  const f = figure(host, 'Egyptian multiplication: doubling and halving',
    'Halve the multiplier (dropping remainders) and double the multiplicand on each row; add the rows whose multiplier is odd. '
    + 'Only doubling, halving and addition are needed.', 'EgyptianMultiplication.multiply()');
  let a = 14, b = 12;
  const show = () => {
    const r = egyptianMultiply({ a, b });
    const plot = document.createElement('div');
    f.out.innerHTML = `<p class="eq">${a} × ${b} = ${r.steps.filter(s => s.include).map(s => s.multiplicand).join(' + ') || 0} = ${r.result}</p>`;
    f.out.appendChild(plot);
    if (r.steps.length) chart(plot, { h: 260, x: { label: 'step', ticks: r.steps.map((_, i) => [i + 1, String(i + 1)]) },
      y: { label: 'multiplicand (doubled each step)' }, title: 'Rows added to the sum (bright) and skipped (dim)',
      series: [{ type: 'bar', x: r.steps.map((_, i) => i + 1), y: r.steps.map(s => s.multiplicand),
        colors: r.steps.map(s => (s.include ? 'var(--accent)' : 'var(--line)')), titles: r.steps.map(s => `${s.multiplicand}`) }] });
    f.out.insertAdjacentHTML('beforeend', table(['Multiplier', 'Multiplicand', 'Include in sum'],
      r.steps.map(s => [s.multiplier, s.multiplicand, s.include ? '<b class="ok">Yes (odd)</b>' : '<span class="mute">No</span>'])));
  };
  numInput(f.ctl, 'Multiplicand', a, v => { a = Math.round(v); show(); }, { min: 0, max: 100000 });
  numInput(f.ctl, 'Multiplier', b, v => { b = Math.round(v); show(); }, { min: 0, max: 100000 });
  checkButton(f, 'egyptian_multiply', () => ({ a, b }), data);
  show();
}

function babylonian(host, data) {
  const f = figure(host, 'Babylonian square root',
    'Start from x = n/2 and replace x by the average of x and n/x. The error (change per step) roughly squares each time, '
    + 'so the digits of √n double: the method stops when a step changes x by less than 1e-10.',
    'BabylonianSquareRoot.calculate()');
  let n = 2, it = 10;
  const show = () => {
    const r = babylonianSqrt({ n, iterations: it });
    f.out.innerHTML = `<p class="eq">x<sub>k+1</sub> = (x<sub>k</sub> + n / x<sub>k</sub>) / 2 &nbsp; → &nbsp; √${fmt(n)} ≈ ${r.result.toPrecision(12)}
      <span class="mute">(Math.sqrt: ${Math.sqrt(n).toPrecision(12)})</span></p><div class="two"><div class="p1"></div><div class="p2"></div></div>`;
    const k = r.steps.map(s => s.iteration);
    if (!k.length) { f.out.insertAdjacentHTML('beforeend', '<p class="mute">√0 = 0: no iterations.</p>'); return; }
    chart(f.out.querySelector('.p1'), { w: 420, h: 280, title: 'Convergence of estimates', x: { label: 'iteration' },
      y: { label: 'estimate' }, series: [{ type: 'line', x: k, y: r.steps.map(s => s.estimate), markers: true, label: 'estimate' },
        { type: 'hline', y: Math.sqrt(n), color: 'var(--accent2)', label: `√${fmt(n)}` }] });
    chart(f.out.querySelector('.p2'), { w: 420, h: 280, title: 'Error convergence', x: { label: 'iteration' },
      y: { label: 'error (log scale)', log: true }, series: [{ type: 'line', x: k, y: r.steps.map(s => s.error), markers: true, color: 'var(--accent3)' }] });
    f.out.insertAdjacentHTML('beforeend', table(['Iteration', 'Estimate', 'Error'],
      r.steps.map(s => [s.iteration, s.estimate.toFixed(6), s.error.toPrecision(6)])));
  };
  const inp = numInput(f.ctl, 'n', n, v => { n = v; show(); }, { min: 0, max: 1e12, step: 'any' });
  sl(f.ctl, 'n (slider, log scale)', -2, 8, 0.01, Math.log10(n), v => { n = +(10 ** v).toPrecision(4); inp.value = n; show(); },
    v => fmt(+(10 ** v).toPrecision(4)));
  sl(f.ctl, 'Max iterations', 1, 30, 1, it, v => { it = v; show(); });
  checkButton(f, 'babylonian_sqrt', () => ({ n, iterations: it }), data);
  show();
}

export function mount(host, { data }) {
  egyptian(host, data);
  babylonian(host, data);
}
