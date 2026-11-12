// Ports of bio_growth_patterns.py (BioGrowthPatterns) and shell_growth_patterns.py (ShellGrowthAnalysis).
// Pure functions; engines.test.mjs compares them with the Python output.
import { linspace, GOLDEN } from './patterns_engine.js';

const rad = d => d * Math.PI / 180;

// BioGrowthPatterns.generate_tree(): recursive binary branching; returns [x0, y0, x1, y1, depth] segments in the
// same (depth-first, left before right) order as the Python list.
export function tree({ branching_angle, depth, length_decay, angle = 90, length = 1 }) {
  const out = [];
  const grow = (x0, y0, ang, len, d) => {
    if (d === 0) return;
    const x1 = x0 + len * Math.cos(rad(ang)), y1 = y0 + len * Math.sin(rad(ang));
    out.push([x0, y0, x1, y1, d]);
    grow(x1, y1, ang + branching_angle, len * length_decay, d - 1);
    grow(x1, y1, ang - branching_angle, len * length_decay, d - 1);
  };
  grow(0, 0, angle, length, depth);
  return out;
}

// BioGrowthPatterns.generate_shell_spiral(): r = a * e^(b * theta), theta from 0 to 6 pi.
export function shellSpiral({ n_points = 1000, growth_rate, tightness }) {
  const th = linspace(0, 6 * Math.PI, n_points);
  const r = th.map(t => tightness * Math.exp(growth_rate * t));
  return { x: th.map((t, i) => r[i] * Math.cos(t)), y: th.map((t, i) => r[i] * Math.sin(t)) };
}

// BioGrowthPatterns.simulate_population_growth(): discrete-time exponential, logistic and Allee models.
export function population({ initial_pop, growth_rate: r, carrying_capacity: K, time_steps, model }) {
  const P = new Array(time_steps).fill(0);
  P[0] = initial_pop;
  const A = initial_pop * 0.5;     // Allee threshold: half the starting population
  for (let t = 1; t < time_steps; t++) {
    const p = P[t - 1];
    if (model === 'exponential') P[t] = p * (1 + r);
    else if (model === 'logistic') P[t] = p + r * p * (1 - p / K);
    else if (model === 'allee') P[t] = p + r * p * ((p - A) / K) * (1 - p / K);
  }
  return P;
}

// ShellGrowthAnalysis.generate_shell_spiral(): r = (e^b)^t over n_whorls turns; z rises with the coiling axis angle.
export function shell3d({ species, n_whorls, n_points = 1000, growth_rate }, table) {
  const p = { ...table[species] };
  if (growth_rate !== undefined) p.growth_rate = growth_rate;
  const t = linspace(0, n_whorls * 2 * Math.PI, n_points), g = Math.exp(p.growth_rate);
  const r = t.map(v => g ** v), tanA = Math.tan(rad(p.coiling_axis));
  return { x: t.map((v, i) => r[i] * Math.cos(v)), y: t.map((v, i) => r[i] * Math.sin(v)),
    z: t.map(v => v * tanA * p.whorl_spacing), metrics: shellMetrics(p) };
}

// ShellGrowthAnalysis.calculate_growth_metrics(): expansion per whorl e^(2 pi b) and its distance from phi.
export function shellMetrics(p) {
  const gr = Math.exp(2 * Math.PI * p.growth_rate);
  return { growth_ratio: gr, golden_ratio_deviation: Math.abs(gr - GOLDEN), whorl_expansion_rate: p.aperture_growth,
    volume_increase_rate: p.aperture_growth ** 3 };
}

// ShellGrowthAnalysis.analyze_surface_pattern(): chamber / rib ripple added to the radius.
export function surfacePattern(kind, r, t) {
  if (kind === 'chambers') return r.map((v, i) => Math.sin(t[i] * 8) * 0.1 * v);
  if (kind === 'ribs') return r.map((v, i) => Math.sin(t[i] * 20) * 0.05 * v);
  return r.map(() => 0);
}
