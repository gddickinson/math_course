// Lesson 7 figures: advanced_tree_patterns.py (AdvancedTreeModel: season, light, nutrients, random variation) and
// tree_data_analysis.py (TreeDataAnalysis: statistics of the script's oak and pine values and the model comparison).
import { esc } from './core.js';
import { advancedTree } from './tree_engine.js';
import { tree } from './growth_engine.js';
import { treeStats, treeCompare } from './stats_engine.js';
import { chart, ramp, PALETTE } from './plot.js';
import { figure, sl, numInput, select, table, num, checkButton } from './ui.js';

// matplotlib colour maps used by visualize_tree() / compare_seasons() (light -> dark with health)
const CMAPS = {
  summer: [[255, 255, 229], [194, 230, 153], [120, 198, 121], [35, 132, 67], [0, 69, 41]],          // YlGn
  spring: [[255, 255, 229], [194, 230, 153], [120, 198, 121], [35, 132, 67], [0, 69, 41]],          // YlGn (health x 1.2)
  autumn: [[255, 255, 204], [254, 217, 118], [253, 141, 60], [227, 26, 28], [128, 0, 38]],         // YlOrRd
  winter: [[247, 251, 255], [198, 219, 239], [107, 174, 214], [33, 113, 181], [8, 48, 107]],        // Blues
};
const MEAS = [['branching_angles', 'Branching angle (°)'], ['length_ratios', 'Length ratio'], ['thickness_ratios', 'Thickness ratio']];

function envTree(host, data) {
  const f = figure(host, 'Tree growth with season, light and nutrients',
    'Each branch splits in two at ± the species\' base angle with random variation (more under stress). Branch length shrinks '
    + 'by the species decay × season growth × light exposure × nutrients; light falls with depth and with the angle away from the light '
    + 'direction, nutrients fall by 10% per level, and branches stop when health drops below 0.1 (winter). Colours use the script\'s '
    + 'season colour maps, reversed for the dark page: lighter = healthier.',
    'AdvancedTreeModel.generate_tree(), calculate_environmental_factor()');
  const s = { species: 'oak', season: 'summer', light_direction: 90, nutrient_level: 1, stress: 0, seed: 1 };
  const show = () => {
    const segs = advancedTree(s, { species: data.tree_species, seasons: data.seasons });
    const cm = CMAPS[s.season], k = s.season === 'spring' ? 1.2 : 1;
    const maxD = segs.reduce((m, d) => Math.max(m, d[4] + 1), 0);
    f.out.innerHTML = `<p class="small mute">${segs.length} branches, ${maxD} levels (species maximum ${data.tree_species[s.species].max_depth}).
      Same tree as <code>random.seed(${s.seed})</code> before <code>generate_tree()</code> in Python.</p><div class="plot sq"></div>`;
    chart(f.out.querySelector('.plot'), { w: 560, h: 520, equal: true, alt: `${s.species} tree in ${s.season}`,
      series: [{ type: 'segments', data: segs.map(d => [d[0], d[1], d[2], d[3], ramp(1 - 0.85 * Math.min(1, d[6] * k), cm), Math.max(0.6, d[5] * 18)]) }] });
  };
  select(f.ctl, 'Species', Object.keys(data.tree_species), s.species, v => { s.species = v; show(); });
  select(f.ctl, 'Season', Object.keys(data.seasons), s.season, v => { s.season = v; show(); });
  sl(f.ctl, 'Light direction (°)', 0, 180, 1, s.light_direction, v => { s.light_direction = v; show(); });
  sl(f.ctl, 'Nutrient level', 0.1, 1, 0.05, s.nutrient_level, v => { s.nutrient_level = v; show(); });
  sl(f.ctl, 'Environmental stress', 0, 2, 0.05, s.stress, v => { s.stress = v; show(); });
  const seed = numInput(f.ctl, 'Random seed', s.seed, v => { s.seed = Math.round(v); show(); }, { min: 0, max: 2 ** 31 });
  const b = document.createElement('button');
  b.className = 'alt'; b.textContent = 'New random tree';
  b.addEventListener('click', () => { s.seed = Math.floor(Math.random() * 1e6); seed.value = s.seed; show(); });
  f.ctl.appendChild(b);
  checkButton(f, 'advanced_tree', () => ({ ...s }), data);
  show();
}

function dataFig(host, data) {
  const f = figure(host, 'Example branching data: summary statistics',
    'Mean, standard deviation and 95% confidence interval (Student t) of the 20 values per measure that the script stores as '
    + 'illustrative example values (not field measurements; no published source). The tree on the right is drawn '
    + 'with the mean angle and mean length ratio, four levels deep, as visualize_example_tree_structure() does.',
    'TreeDataAnalysis.analyze_branching_patterns(), visualize_example_tree_structure()');
  let sp = 'oak';
  const show = () => {
    const st = treeStats({ species: sp }, data.tree_data), d = data.tree_data[sp];
    f.out.innerHTML = table(['Measure', 'Mean', 'Std dev', '95% CI'], MEAS.map(([k, t]) => [t, num(st[k].mean, 3), num(st[k].std, 3),
      `${num(st[k].ci[0], 3)} – ${num(st[k].ci[1], 3)}`])) + '<div class="two"><div class="p1"></div><div class="p2"></div></div>';
    const lo = Math.min(...d.branching_angles), hi = Math.max(...d.branching_angles), bins = 15, w = (hi - lo) / bins;
    const cnt = new Array(bins).fill(0);
    d.branching_angles.forEach(v => { cnt[Math.min(bins - 1, Math.floor((v - lo) / w))]++; });
    chart(f.out.querySelector('.p1'), { w: 420, h: 300, title: 'Branching angle distribution', x: { label: 'angle (degrees)' },
      y: { label: 'density' }, series: [{ type: 'bar', barWidth: w * 0.9, x: cnt.map((_, i) => lo + (i + 0.5) * w),
        y: cnt.map(c => c / (d.branching_angles.length * w)), color: 'var(--accent3)' }] });
    const segs = tree({ branching_angle: st.branching_angles.mean, depth: 4, length_decay: st.length_ratios.mean });
    chart(f.out.querySelector('.p2'), { w: 420, h: 300, equal: true, title: `${sp} structure from the means`,
      series: [{ type: 'segments', data: segs.map(s => [s[0], s[1], s[2], s[3], '#c08a5a', 1 + s[4]]) }] });
  };
  select(f.ctl, 'Species', Object.keys(data.tree_data), sp, v => { sp = v; show(); });
  checkButton(f, 'tree_stats', () => ({ species: sp }), data);
  show();
}

function compareFig(host, data) {
  const f = figure(host, 'Example data versus the model',
    'The script draws 20 model values per measure from a normal distribution around the model parameters (oak 35°, 0.75, 0.6; '
    + 'pine 45°, 0.8, 0.7) and compares them with the example values by a two-sample t-test and Cohen\'s d. The draws are random: '
    + 'the seed here reproduces <code>np.random.seed(seed)</code> in Python.', 'TreeDataAnalysis.compare_with_model(), visualize_comparisons()');
  const s = { species: 'oak', seed: 1 };
  const show = () => {
    const r = treeCompare(s, data.tree_data), real = data.tree_data[s.species];
    f.out.innerHTML = table(['Measure', 't statistic', 'p value', 'Effect size d'], MEAS.map(([k, t]) => {
      const c = r.comparisons[k];
      return [t, num(c.t_statistic, 3), `${num(c.p_value, 4)}${c.p_value < 0.05 ? ' <span class="pink">(&lt; 0.05)</span>' : ''}`, num(c.effect_size, 3)];
    })) + `<div class="three">${MEAS.map((_, i) => `<div class="m${i}"></div>`).join('')}</div>`;
    MEAS.forEach(([k, t], i) => {
      const jit = (n, c) => Array.from({ length: n }, (_, j) => c + ((j * 7919) % 13 - 6) / 30);
      chart(f.out.querySelector(`.m${i}`), { w: 300, h: 280, title: t, x: { min: 0.4, max: 2.6, ticks: [[1, 'example data'], [2, 'model']] },
        series: [{ type: 'scatter', x: jit(real[k].length, 1), y: real[k], color: PALETTE[2], r: 3 },
          { type: 'scatter', x: jit(r.model[k].length, 2), y: r.model[k], color: PALETTE[0], r: 3 }] });
    });
  };
  select(f.ctl, 'Species', Object.keys(data.tree_data), s.species, v => { s.species = v; show(); });
  const seed = numInput(f.ctl, 'Random seed', s.seed, v => { s.seed = Math.round(v); show(); }, { min: 0, max: 2 ** 31 });
  const b = document.createElement('button');
  b.className = 'alt'; b.textContent = 'New model draw';
  b.addEventListener('click', () => { s.seed = Math.floor(Math.random() * 1e6); seed.value = s.seed; show(); });
  f.ctl.appendChild(b);
  checkButton(f, 'tree_compare', () => ({ ...s }), data);
  show();
}

export function mount(host, { data }) {
  envTree(host, data);
  dataFig(host, data);
  compareFig(host, data);
  host.insertAdjacentHTML('beforeend', `<p class="small mute">Species parameters: ${esc(Object.entries(data.tree_species)
    .map(([k, p]) => `${k} ${p.base_angle}°, decay ${p.length_decay}, depth ${p.max_depth}`).join(' · '))}.</p>`);
}
