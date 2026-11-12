// Statistics used by tree_data_analysis.py and shell_comparative_analysis.py, ported from numpy/scipy:
// mean, std, sem, Student t distribution (cdf/ppf via the regularized incomplete beta), stats.t.interval,
// stats.ttest_ind (equal variances), Cohen's d as the script computes it, and stats.pearsonr (r and two-sided p).
import { NpRandom } from './pyrandom.js';

export const mean = a => a.reduce((s, v) => s + v, 0) / a.length;
export const variance = (a, ddof = 0) => { const m = mean(a); return a.reduce((s, v) => s + (v - m) ** 2, 0) / (a.length - ddof); };
export const std = (a, ddof = 0) => Math.sqrt(variance(a, ddof));
export const sem = a => std(a, 1) / Math.sqrt(a.length);

// log-gamma (Lanczos, g = 7, n = 9; ~1e-15 relative)
const LG = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059,
  12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
export function lgamma(x) {
  if (x < 0.5) return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * x))) - lgamma(1 - x);
  x -= 1;
  let a = LG[0];
  const t = x + 7.5;
  for (let i = 1; i < 9; i++) a += LG[i] / (x + i);
  return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(a);
}

// continued fraction for the incomplete beta (modified Lentz)
function betacf(a, b, x) {
  const TINY = 1e-300;
  let c = 1, d = 1 - (a + b) * x / (a + 1);
  if (Math.abs(d) < TINY) d = TINY;
  d = 1 / d;
  let h = d;
  for (let m = 1; m <= 1000; m++) {
    const m2 = 2 * m;
    let aa = m * (b - m) * x / ((a + m2 - 1) * (a + m2));
    d = 1 + aa * d; if (Math.abs(d) < TINY) d = TINY; c = 1 + aa / c; if (Math.abs(c) < TINY) c = TINY;
    d = 1 / d; h *= d * c;
    aa = -(a + m) * (a + b + m) * x / ((a + m2) * (a + m2 + 1));
    d = 1 + aa * d; if (Math.abs(d) < TINY) d = TINY; c = 1 + aa / c; if (Math.abs(c) < TINY) c = TINY;
    d = 1 / d;
    const del = d * c;
    h *= del;
    if (Math.abs(del - 1) < 1e-16) break;
  }
  return h;
}

// regularized incomplete beta I_x(a, b)
export function betainc(a, b, x) {
  if (x <= 0) return 0;
  if (x >= 1) return 1;
  const bt = Math.exp(lgamma(a + b) - lgamma(a) - lgamma(b) + a * Math.log(x) + b * Math.log1p(-x));
  return x < (a + 1) / (a + b + 2) ? bt * betacf(a, b, x) / a : 1 - bt * betacf(b, a, 1 - x) / b;
}

// Student t: two-sided tail P(|T| > |t|), cdf and ppf
export const tTwoSided = (t, df) => betainc(df / 2, 0.5, df / (df + t * t));
export const tCdf = (t, df) => (t >= 0 ? 1 - 0.5 * tTwoSided(t, df) : 0.5 * tTwoSided(t, df));
export function tPpf(q, df) {
  if (q === 0.5) return 0;
  if (q < 0.5) return -tPpf(1 - q, df);
  let lo = 0, hi = 1;
  while (tCdf(hi, df) < q) hi *= 2;
  for (let i = 0; i < 200 && hi - lo > 1e-15 * hi; i++) { const mid = (lo + hi) / 2; if (tCdf(mid, df) < q) lo = mid; else hi = mid; }
  return (lo + hi) / 2;
}

// stats.t.interval(conf, n-1, loc=mean, scale=sem)
export function tInterval(a, conf = 0.95) {
  const m = mean(a), h = tPpf(0.5 + conf / 2, a.length - 1) * sem(a);
  return [m - h, m + h];
}

// stats.ttest_ind(a, b) (pooled variance) -> [t, two-sided p]
export function ttestInd(a, b) {
  const n1 = a.length, n2 = b.length, df = n1 + n2 - 2;
  const sp = ((n1 - 1) * variance(a, 1) + (n2 - 1) * variance(b, 1)) / df;
  const t = (mean(a) - mean(b)) / Math.sqrt(sp * (1 / n1 + 1 / n2));
  return [t, tTwoSided(t, df)];
}

// stats.pearsonr(x, y) -> [r, two-sided p]
export function pearsonr(x, y) {
  const mx = mean(x), my = mean(y);
  let sxy = 0, sxx = 0, syy = 0;
  for (let i = 0; i < x.length; i++) { const dx = x[i] - mx, dy = y[i] - my; sxy += dx * dy; sxx += dx * dx; syy += dy * dy; }
  const r = Math.max(-1, Math.min(1, sxy / Math.sqrt(sxx * syy))), df = x.length - 2;
  return [r, betainc(df / 2, 0.5, 1 - r * r)];
}

const MEASURES = ['branching_angles', 'length_ratios', 'thickness_ratios'];

// TreeDataAnalysis.analyze_branching_patterns()
export function treeStats({ species }, data) {
  const d = data[species];
  return Object.fromEntries(MEASURES.map(k => [k, { mean: mean(d[k]), std: std(d[k]), ci: tInterval(d[k]) }]));
}

// TreeDataAnalysis.generate_model_predictions() after np.random.seed(seed), and compare_with_model()
export const MODEL_BASE = { oak: [35, 0.75, 0.6], pine: [45, 0.8, 0.7] };
export function treeCompare({ species, seed }, data, n = 20) {
  const rs = new NpRandom(seed), [ang, len, th] = MODEL_BASE[species] || MODEL_BASE.pine;
  const model = { branching_angles: rs.normal(0, 2, n).map(v => ang + v),
    length_ratios: rs.normal(0, 0.02, n).map(v => len + v), thickness_ratios: rs.normal(0, 0.02, n).map(v => th + v) };
  const comparisons = {};
  for (const k of MEASURES) {
    const real = data[species][k], [t, p] = ttestInd(real, model[k]);
    const d = (mean(real) - mean(model[k])) / Math.sqrt((variance(real) + variance(model[k])) / 2);
    comparisons[k] = { t_statistic: t, p_value: p, effect_size: d };
  }
  return { model, comparisons };
}

// ShellComparativeAnalysis.analyze_temperature_effects() and compare_modern_fossil() for every species
export function shellStats(_, shellData) {
  const all = Object.values(shellData).flatMap(sp => Object.values(sp).flat());
  const T = all.map(m => m.temperature), G = all.map(m => m.growth_rate), S = all.map(m => m.size);
  const compare = {};
  for (const [sp, d] of Object.entries(shellData)) {
    const mo = d.modern || [], fo = d.fossil || [];
    if (!mo.length || !fo.length) { compare[sp] = { error: 'Insufficient data for comparison' }; continue; }
    const avg = (ms, k) => mean(ms.map(m => m[k]));
    const c = { modern: {}, fossil: {}, differences: {} };
    for (const k of ['size', 'growth_rate', 'thickness']) {
      c.modern[k] = avg(mo, k); c.fossil[k] = avg(fo, k);
      c.differences[k] = (c.modern[k] - c.fossil[k]) / c.fossil[k] * 100;
    }
    compare[sp] = c;
  }
  return { temperature_growth_correlation: pearsonr(T, G), temperature_size_correlation: pearsonr(T, S),
    mean_growth_rate: mean(G), mean_temperature: mean(T), compare };
}
