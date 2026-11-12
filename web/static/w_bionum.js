// Lesson 4 figures: bio_number_theory.py (BioNumberTheory): prime cicada life cycles against predator cycles, DNA
// length factorization, and common factors of several sequence lengths.
import { esc } from './core.js';
import { cicada, dnaLength, geneticSequences } from './numtheory_engine.js';
import { chart } from './plot.js';
import { figure, sl, numInput, textInput, checkbox, table, kv, num, checkButton } from './ui.js';

function cicadaFig(host, data) {
  const f = figure(host, 'Why prime life cycles? Cicadas and predators',
    'A cicada brood with a cycle of c years meets a predator with a cycle of p years every lcm(c, p) years. The script counts '
    + 'the meetings over the time span and scores fitness as 1 / (encounters + 1); prime cycles are drawn in pink.',
    'BioNumberTheory.simulate_cicada_lifecycle(), visualize_cicada_fitness()');
  let years = 100;
  const pred = new Set([2, 3, 4, 6, 8, 9, 10]);   // the script's example predator cycles
  const show = () => {
    const r = cicada({ years, predators: [...pred] });
    f.out.innerHTML = '<div class="plot"></div>';
    chart(f.out.querySelector('.plot'), { h: 290, title: 'Relative fitness of cicada life-cycle lengths',
      x: { label: 'cycle length (years)', ticks: r.map(c => [c.cycle, String(c.cycle)]) }, y: { label: 'relative fitness' },
      series: [{ type: 'bar', x: r.map(c => c.cycle), y: r.map(c => c.relative_fitness),
        colors: r.map(c => (c.is_prime ? 'var(--accent2)' : 'var(--accent3)')), titles: r.map(c => `${c.encounters} encounters`) },
      { type: 'bar', x: [], y: [], color: 'var(--accent2)', label: 'prime cycle' }, { type: 'bar', x: [], y: [], color: 'var(--accent3)', label: 'non-prime' }] });
    f.out.insertAdjacentHTML('beforeend', table(['Cycle', 'Prime', 'Encounters', 'Relative fitness'],
      r.map(c => [c.cycle, c.is_prime ? '<b class="pink">yes</b>' : 'no', c.encounters, num(c.relative_fitness)])));
  };
  sl(f.ctl, 'Time span (years)', 17, 1000, 1, years, v => { years = v; show(); });
  const box = document.createElement('fieldset');
  box.className = 'preds';
  box.innerHTML = '<legend class="small mute">Predator cycles (years)</legend>';
  f.ctl.appendChild(box);
  for (let p = 2; p <= 12; p++) checkbox(box, String(p), pred.has(p), on => { if (on) pred.add(p); else pred.delete(p); show(); });
  checkButton(f, 'cicada', () => ({ years, predators: [...pred] }), data);
  show();
}

function pie(fac) {
  const tot = fac.reduce((s, [, e]) => s + e, 0), C = ['var(--accent)', 'var(--accent2)', 'var(--accent3)', 'var(--warn)', '#b388ff', '#ff9e57'];
  let a0 = -Math.PI / 2;
  const parts = fac.map(([p, e], i) => {
    const a1 = a0 + 2 * Math.PI * e / tot, big = a1 - a0 > Math.PI ? 1 : 0;
    const P = a => `${100 + 80 * Math.cos(a)},${100 + 80 * Math.sin(a)}`;
    const mid = (a0 + a1) / 2, d = fac.length === 1 ? '<circle cx="100" cy="100" r="80"' : `<path d="M100,100 L${P(a0)} A80,80 0 ${big} 1 ${P(a1)} Z"`;
    const s = `${d} style="fill:${C[i % C.length]}" fill-opacity=".75"/><text x="${100 + 52 * Math.cos(mid)}" y="${104 + 52 * Math.sin(mid)}" text-anchor="middle">${p}</text>`;
    a0 = a1;
    return s;
  });
  return `<svg class="pie" viewBox="0 0 200 200" role="img" aria-label="share of each prime in the factorization">${parts.join('')}</svg>`;
}

function dnaFig(host, data) {
  const f = figure(host, 'DNA sequence length: factors, codons and nucleosomes',
    'The script factorizes a length in base pairs, checks divisibility by 3 (codons) and compares it with the 147 bp nucleosome unit. '
    + 'The pie shows each prime\'s exponent as its share, as in visualize_dna_factorization().', 'BioNumberTheory.analyze_dna_length()');
  let L = 3456;
  const show = () => {
    const r = dnaLength({ length: L });
    f.out.innerHTML = `<div class="two"><div>${kv([['Factorization', r.factors.map(([p, e]) => `${p}<sup>${e}</sup>`).join(' × ') || '–'],
      ['Divisible by 3', r.is_multiple_3 ? 'yes' : 'no'], ['Nucleosome units (length / 147)', num(r.possible_nucleosome_units, 3)]])}
      <h3>Implications printed by the script</h3>${r.implications.length ? `<ul>${r.implications.map(i => `<li>${esc(i)}</li>`).join('')}</ul>` : '<p class="mute">none</p>'}</div>
      <div>${r.factors.length ? pie(r.factors) : ''}</div></div>`;
  };
  numInput(f.ctl, 'Length (bp)', L, v => { L = Math.round(v); show(); }, { min: 1, max: 1e9 });
  checkButton(f, 'dna_length', () => ({ length: L }), data);
  show();
}

function seqFig(host, data) {
  const f = figure(host, 'Several sequence lengths: common units',
    'GCD, LCM and all common factors of the lengths; a common factor 3 means every length could be read in whole codons.',
    'BioNumberTheory.analyze_genetic_sequences()');
  let txt = '612, 918, 1224';
  const show = () => {
    const lengths = txt.split(/[\s,;]+/).map(Number).filter(v => Number.isInteger(v) && v > 0).slice(0, 20);
    if (!lengths.length) { f.out.innerHTML = '<p class="mute">Enter positive whole numbers.</p>'; return; }
    const r = geneticSequences({ lengths });
    f.out.innerHTML = kv([['Lengths', lengths.join(', ')], ['GCD', r.gcd], ['LCM', r.lcm.toLocaleString('en')],
      ['Common factors', r.common_factors.join(', ')], ['Patterns', r.patterns.map(esc).join('<br>') || '–']]);
  };
  textInput(f.ctl, 'Lengths (comma separated)', txt, v => { txt = v; show(); });
  checkButton(f, 'genetic_sequences', () => ({ lengths: txt.split(/[\s,;]+/).map(Number).filter(v => Number.isInteger(v) && v > 0).slice(0, 20) }), data);
  show();
}

export function mount(host, { data }) {
  cicadaFig(host, data);
  dnaFig(host, data);
  seqFig(host, data);
}
