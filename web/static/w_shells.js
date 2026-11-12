// Lesson 8 figures: shell_growth_patterns.py (ShellGrowthAnalysis: species spirals in top and side view, growth
// metrics) and shell_comparative_analysis.py (ShellComparativeAnalysis: temperature correlations, modern vs fossil).
import { esc } from './core.js';
import { shell3d } from './growth_engine.js';
import { shellStats } from './stats_engine.js';
import { chart, ramp, PALETTE } from './plot.js';
import { figure, sl, select, table, num, checkButton } from './ui.js';

function spiralFig(host, data) {
  const f = figure(host, 'Shell spirals by species: top and side view',
    'r = (e^b)^t for t over n whorls; species with a tilted coiling axis (the Turritella gastropod, 15°) also rise along z = t·tan(axis)·whorl spacing. '
    + 'Growth ratio = e^(2πb), the radius factor per whorl, and its distance from φ ≈ 1.618 are the script\'s metrics. Dot colour = height.',
    'ShellGrowthAnalysis.generate_shell_spiral(), calculate_growth_metrics(), visualize_shell()');
  const s = { species: 'nautilus', n_whorls: 4, n_points: 1000 };
  let b = data.shell_species.nautilus.growth_rate;
  const show = () => {
    const p = { ...s, growth_rate: b }, r = shell3d(p, data.shell_species), sp = data.shell_species[s.species];
    const zmax = Math.max(...r.z, 1e-9), m = r.metrics;
    f.out.innerHTML = `<p class="small"><b>${esc(sp.species)}</b> · surface: ${esc(sp.surface_pattern)} · coiling axis ${sp.coiling_axis}°</p>
      <div class="two"><div class="p1"></div><div class="p2"></div></div>` + table(['Metric', 'Value'], [
      ['Growth ratio e^(2πb)', num(m.growth_ratio, 3)], ['Golden ratio deviation |ratio − φ|', num(m.golden_ratio_deviation, 3)],
      ['Whorl expansion rate', num(m.whorl_expansion_rate, 3)], ['Volume increase rate', num(m.volume_increase_rate, 3)]]);
    const col = r.z.map(z => ramp(0.35 + 0.65 * z / zmax));
    chart(f.out.querySelector('.p1'), { w: 420, h: 400, equal: true, title: 'Top view (x, y)',
      series: [{ type: 'scatter', x: r.x, y: r.y, colors: col, r: 1.8 }] });
    chart(f.out.querySelector('.p2'), { w: 420, h: 400, title: 'Side view (x, z)', x: { label: 'x' }, y: { label: 'z (height)' },
      series: [{ type: 'line', x: r.x, y: r.z, color: 'var(--accent3)', width: 1.2 }] });
  };
  const bs = sl(f.ctl, 'Growth rate b', 0.05, 0.35, 0.001, b, v => { b = v; show(); });
  select(f.ctl, 'Species', Object.keys(data.shell_species), s.species, v => {
    s.species = v; b = data.shell_species[v].growth_rate; bs.value = b; bs.dispatchEvent(new Event('input'));
  });
  sl(f.ctl, 'Whorls (growth stage)', 0.5, 6, 0.1, s.n_whorls, v => { s.n_whorls = v; show(); });
  const p = document.createElement('p');
  p.className = 'small mute';
  p.textContent = `Golden spiral for comparison: b = ln(φ)/(π/2) ≈ ${(Math.log((1 + Math.sqrt(5)) / 2) / (Math.PI / 2)).toFixed(3)}.`;
  f.ctl.appendChild(p);
  checkButton(f, 'shell3d', () => ({ ...s, growth_rate: b }), data);
  show();
}

function compareFig(host, data) {
  const f = figure(host, 'Shell measurements: temperature, size and age',
    'The values and the citations are those written in shell_comparative_analysis.py ("Real measurement data compiled from research papers"); '
    + 'they are not checked here. Pearson correlations over all specimens, and modern versus fossil means with the % change.',
    'ShellComparativeAnalysis.analyze_temperature_effects(), compare_modern_fossil()');
  const D = data.shell_data, r = shellStats({}, D);
  const all = Object.entries(D).flatMap(([sp, per]) => Object.entries(per).flatMap(([p, ms]) => ms.map(m => ({ ...m, sp, p }))));
  const groups = [...new Set(all.map(m => `${m.sp} (${m.p})`))];
  const series = key => groups.map((g, i) => {
    const ms = all.filter(m => `${m.sp} (${m.p})` === g);
    return { type: 'scatter', x: ms.map(m => m.temperature), y: ms.map(m => m[key]), color: PALETTE[i % PALETTE.length], label: g, r: g.includes('fossil') ? 4 : 5 };
  });
  const [rg, pg] = r.temperature_growth_correlation, [rs, ps] = r.temperature_size_correlation;
  f.out.innerHTML = `<div class="two"><div class="p1"></div><div class="p2"></div></div>
    <p>Temperature–growth correlation r = ${num(rg, 3)} (p = ${num(pg, 3)}); temperature–size r = ${num(rs, 3)} (p = ${num(ps, 3)});
    ${all.length} specimens, mean growth rate ${num(r.mean_growth_rate, 4)}, mean temperature ${num(r.mean_temperature, 1)} °C.</p>
    <div class="three"><div class="b0"></div><div class="b1"></div><div class="b2"></div></div>`
    + table(['Species', 'Size change', 'Growth-rate change', 'Thickness change'], Object.entries(r.compare).map(([sp, c]) =>
      (c.error ? [sp, `<span class="mute">${esc(c.error)}</span>`, '', '']
        : [sp, ...['size', 'growth_rate', 'thickness'].map(k => `${c.differences[k] > 0 ? '+' : ''}${c.differences[k].toFixed(1)}%`)])))
    + table(['Species', 'Period', 'Size (mm)', 'Whorls', 'Growth rate', 'Temp (°C)', 'Thickness (mm)', 'Location', 'Source (as cited in the script)'],
      all.map(m => [esc(m.species), esc(m.age), m.size, m.whorl_count, m.growth_rate, m.temperature, m.thickness, esc(m.location), esc(m.source)]), 'small');
  chart(f.out.querySelector('.p1'), { w: 420, h: 300, title: 'Temperature effect on growth rate', x: { label: 'temperature (°C)' },
    y: { label: 'growth rate' }, series: series('growth_rate') });
  chart(f.out.querySelector('.p2'), { w: 420, h: 300, title: 'Temperature effect on size', x: { label: 'temperature (°C)' },
    y: { label: 'size (mm)' }, series: series('size') });
  const both = Object.entries(r.compare).filter(([, c]) => !c.error);
  [['size', 'Size (mm)'], ['growth_rate', 'Growth rate'], ['thickness', 'Thickness (mm)']].forEach(([k, t], i) => {
    chart(f.out.querySelector(`.b${i}`), { w: 300, h: 260, title: t, x: { ticks: both.map(([sp], j) => [j, sp]) }, y: { min: 0 },
      series: [{ type: 'bar', barWidth: 0.35, offset: -0.2, x: both.map((_, j) => j), y: both.map(([, c]) => c.modern[k]), color: '#7fd4ff', label: 'modern' },
        { type: 'bar', barWidth: 0.35, offset: 0.2, x: both.map((_, j) => j), y: both.map(([, c]) => c.fossil[k]), color: '#9be7a0', label: 'fossil' }] });
  });
  checkButton(f, 'shell_stats', () => ({}), data);
}

export function mount(host, { data }) {
  spiralFig(host, data);
  compareFig(host, data);
}
