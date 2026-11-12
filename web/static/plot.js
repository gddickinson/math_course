// Tiny SVG charting for the lesson figures (no library): line, scatter, bar and segment series on linear or log axes,
// optional equal aspect for geometric drawings (trees, spirals). Colours are CSS colours or var(--...) tokens.
import { esc } from './core.js';

const VIRIDIS = [[68, 1, 84], [59, 82, 139], [33, 145, 140], [94, 201, 98], [253, 231, 37]];
// viridis-like ramp, t in [0, 1]
export function ramp(t, stops = VIRIDIS) {
  t = Math.max(0, Math.min(1, t)) * (stops.length - 1);
  const i = Math.min(stops.length - 2, Math.floor(t)), f = t - i;
  const c = stops[i].map((v, k) => Math.round(v + (stops[i + 1][k] - v) * f));
  return `rgb(${c.join(',')})`;
}
export const PALETTE = ['var(--accent)', 'var(--accent2)', 'var(--accent3)', 'var(--warn)', '#b388ff', '#ff9e57'];

function niceStep(span, n) {
  const raw = span / Math.max(1, n), mag = 10 ** Math.floor(Math.log10(raw)), f = raw / mag;
  return (f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10) * mag;
}
export function fmt(v) {
  if (v === 0) return '0';
  const a = Math.abs(v);
  if (a >= 1e5 || a < 1e-3) return v.toExponential(a >= 1e5 ? 2 : 0).replace('e+', 'e').replace(/\.?0+e/, 'e');
  return String(+v.toPrecision(4));
}

function extent(series, key, log) {
  let lo = Infinity, hi = -Infinity;
  for (const s of series) {
    const vals = s.type === 'segments' ? s.data.flatMap(d => (key === 'x' ? [d[0], d[2]] : [d[1], d[3]]))
      : s.type === 'hline' ? (key === 'y' ? [s.y] : []) : s[key];
    for (const v of vals || []) if (Number.isFinite(v) && (!log || v > 0)) { lo = Math.min(lo, v); hi = Math.max(hi, v); }
    if (s.type === 'bar' && key === 'y' && !log) lo = Math.min(lo, 0);
  }
  if (!Number.isFinite(lo)) { lo = log ? 1 : 0; hi = log ? 10 : 1; }
  if (lo === hi) { const d = log ? lo : Math.abs(lo) * 0.1 || 1; lo -= log ? lo * 0.5 : d; hi += d; }
  return [lo, hi];
}

// chart(host, opts): opts = { w, h, title, x: {label, min, max, log, ticks:[[v,label]]}, y: {...}, equal, legend,
//   series: [{ type: 'line'|'scatter'|'bar'|'segments'|'hline', x, y, color, colors, label, r, width, dash, data }] }
export function chart(host, o) {
  const W = o.w || 640, H = o.h || 320, m = { l: o.ml ?? (o.equal ? 14 : 58), r: 14, t: o.title ? 28 : 12, b: o.equal ? 14 : 44 };
  const xs = o.x || {}, ys = o.y || {};
  let [x0, x1] = [xs.min, xs.max], [y0, y1] = [ys.min, ys.max];
  const ex = extent(o.series, 'x', xs.log), ey = extent(o.series, 'y', ys.log);
  const pad = ([a, b], log) => (log ? [a / 1.3, b * 1.3] : [a - (b - a) * 0.04, b + (b - a) * 0.04]);
  const bars = o.series.some(s => s.type === 'bar');
  const px = o.equal || bars ? ex : pad(ex, xs.log), py = o.equal ? ey : bars ? [ey[0], ey[1] + (ey[1] - ey[0]) * 0.04] : pad(ey, ys.log);
  x0 ??= px[0]; x1 ??= px[1]; y0 ??= py[0]; y1 ??= py[1];
  if (o.series.some(s => s.type === 'bar') && xs.min === undefined) { x0 -= 0.6; x1 += 0.6; }
  const pw = W - m.l - m.r, ph = H - m.t - m.b;
  if (o.equal) {   // same scale on both axes, centred
    const s = Math.max((x1 - x0) / pw, (y1 - y0) / ph) * 1.04, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    [x0, x1, y0, y1] = [cx - s * pw / 2, cx + s * pw / 2, cy - s * ph / 2, cy + s * ph / 2];
  }
  const L = v => Math.log10(v);
  const X = v => m.l + (xs.log ? (L(v) - L(x0)) / (L(x1) - L(x0)) : (v - x0) / (x1 - x0)) * pw;
  const Y = v => m.t + ph - (ys.log ? (L(v) - L(y0)) / (L(y1) - L(y0)) : (v - y0) / (y1 - y0)) * ph;
  const ticks = (lo, hi, log, n) => {
    if (log) { const out = []; for (let e = Math.ceil(L(lo)); e <= Math.floor(L(hi)); e++) out.push(10 ** e);
      const k = Math.ceil(out.length / n); return out.filter((_, i) => i % k === 0); }
    const st = niceStep(hi - lo, n), out = [];
    for (let v = Math.ceil(lo / st) * st; v <= hi + st * 1e-9; v += st) out.push(Math.abs(v) < st * 1e-9 ? 0 : v);
    return out;
  };
  const g = [];
  if (!o.equal) {
    for (const v of ys.ticks ? ys.ticks.map(t => t[0]) : ticks(y0, y1, ys.log, 5)) {
      g.push(`<line class="gl" x1="${m.l}" x2="${m.l + pw}" y1="${Y(v)}" y2="${Y(v)}"/>`,
        `<text class="tk" x="${m.l - 6}" y="${Y(v) + 4}" text-anchor="end">${esc(ys.ticks?.find(t => t[0] === v)?.[1] ?? fmt(v))}</text>`);
    }
    for (const v of xs.ticks ? xs.ticks.map(t => t[0]) : ticks(x0, x1, xs.log, Math.max(3, Math.floor(pw / 80)))) {
      g.push(`<line class="gl" y1="${m.t}" y2="${m.t + ph}" x1="${X(v)}" x2="${X(v)}"/>`,
        `<text class="tk" y="${m.t + ph + 16}" x="${X(v)}" text-anchor="middle">${esc(xs.ticks?.find(t => t[0] === v)?.[1] ?? fmt(v))}</text>`);
    }
    g.push(`<rect class="frame" x="${m.l}" y="${m.t}" width="${pw}" height="${ph}"/>`);
    if (xs.label) g.push(`<text class="al" x="${m.l + pw / 2}" y="${H - 6}" text-anchor="middle">${esc(xs.label)}</text>`);
    if (ys.label) g.push(`<text class="al" transform="translate(13 ${m.t + ph / 2}) rotate(-90)" text-anchor="middle">${esc(ys.label)}</text>`);
  }
  const body = [];
  o.series.forEach((s, si) => {
    const col = s.color || PALETTE[si % PALETTE.length];
    if (s.type === 'line') {
      const pts = s.x.map((v, i) => [v, s.y[i]]).filter(([a, b]) => Number.isFinite(a) && Number.isFinite(b) && (!ys.log || b > 0));
      body.push(`<polyline fill="none" style="stroke:${col}" stroke-width="${s.width || 2}" ${s.dash ? `stroke-dasharray="${s.dash}"` : ''}
        points="${pts.map(([a, b]) => `${X(a).toFixed(1)},${Y(b).toFixed(1)}`).join(' ')}"/>`);
      if (s.markers) pts.forEach(([a, b]) => body.push(`<circle cx="${X(a)}" cy="${Y(b)}" r="3" style="fill:${col}"/>`));
    } else if (s.type === 'scatter') {
      s.x.forEach((v, i) => { if (Number.isFinite(v) && Number.isFinite(s.y[i])) body.push(
        `<circle cx="${X(v).toFixed(1)}" cy="${Y(s.y[i]).toFixed(1)}" r="${s.r || 3}" style="fill:${s.colors ? s.colors[i] : col}" fill-opacity="${s.alpha ?? 0.85}"/>`); });
    } else if (s.type === 'bar') {
      const bw = s.barWidth || 0.8;
      s.x.forEach((v, i) => { const ya = Y(ys.log ? y0 : Math.max(y0, 0)), yb = Y(s.y[i]);
        body.push(`<rect x="${X(v - bw / 2 + (s.offset || 0))}" width="${Math.max(1, X(v + bw / 2) - X(v - bw / 2))}" y="${Math.min(ya, yb)}"
          height="${Math.abs(ya - yb)}" style="fill:${s.colors ? s.colors[i] : col}" fill-opacity="${s.alpha ?? 0.8}"><title>${esc(s.titles ? s.titles[i] : fmt(s.y[i]))}</title></rect>`); });
    } else if (s.type === 'segments') {
      for (const d of s.data) body.push(`<line x1="${X(d[0]).toFixed(1)}" y1="${Y(d[1]).toFixed(1)}" x2="${X(d[2]).toFixed(1)}" y2="${Y(d[3]).toFixed(1)}"
        style="stroke:${d[4] || col}" stroke-width="${d[5] || 1.5}" stroke-linecap="round"/>`);
    } else if (s.type === 'hline') {
      body.push(`<line x1="${m.l}" x2="${m.l + pw}" y1="${Y(s.y)}" y2="${Y(s.y)}" style="stroke:${col}" stroke-dasharray="6 4" stroke-width="1.5"/>`);
    }
  });
  const named = o.series.map((s, i) => [s, s.color || PALETTE[i % PALETTE.length]]).filter(([s]) => s.label);
  const legend = named.length ? `<div class="legend">${named.map(([s, c]) => `<span><i style="background:${c}"></i>${esc(s.label)}</span>`).join('')}</div>` : '';
  host.innerHTML = `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(o.title || o.alt || 'chart')}">
    ${o.title ? `<text class="ttl" x="${W / 2}" y="18" text-anchor="middle">${esc(o.title)}</text>` : ''}
    ${g.join('')}<svg x="${m.l}" y="${m.t}" width="${pw}" height="${ph}" viewBox="${m.l} ${m.t} ${pw} ${ph}" overflow="hidden">${body.join('')}</svg></svg>${legend}`;
}
